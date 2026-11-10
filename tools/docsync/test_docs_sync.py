from __future__ import annotations

import io
import subprocess
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.docsync import docs_sync


def marker_reply(n: int) -> str:
    # Dragonfly upper-cases the unknown command name in its error.
    return f"(error) ERR unknown command `__DOCSYNC_SEP_{n}__`"


class FakeDockerSession:
    """Plays `redis-cli --no-raw` reading a session script on stdin, against
    a tiny in-memory server. Keys go away on FLUSHALL, ACL users do not."""

    def __init__(self, timeout_on: str | None = None, drop_connection_on: str | None = None,
                 flush_reply: str = "OK") -> None:
        self.scripts: list[str] = []
        self.calls: list[list[str]] = []
        self.timeout_on = timeout_on
        # redis-cli loses the connection on this line: no reply, a stderr line.
        self.drop_connection_on = drop_connection_on
        self.flush_reply = flush_reply
        self.store: dict[str, str] = {}
        self.users: list[str] = []

    def run_session(self, script: str) -> docs_sync.SessionRun:
        self.scripts.append(script)
        out: list[str] = []
        stderr = ""
        in_multi = False
        queued: list[str] = []
        for line in script.splitlines():
            if line == self.timeout_on:
                return docs_sync.SessionRun("\n".join(out) + "\n", "", 124, True)
            if line == self.drop_connection_on:
                stderr = "Error: Server closed the connection\n"
                continue
            name = line.split()[0].upper()
            if name.startswith("__DOCSYNC_SEP_"):
                out.append(f"(error) ERR unknown command `{name}`")
            elif in_multi and name in ("EXEC", "DISCARD", "RESET"):
                in_multi = False
                if name == "EXEC":
                    replies = [self.reply(q)[0] for q in queued]
                    out.extend(f"{i}) {r}" for i, r in enumerate(replies, 1))
                else:
                    out.append("OK" if name == "DISCARD" else "RESET")
                queued = []
            elif in_multi:
                if name == "MULTI":
                    out.append("(error) ERR MULTI calls can not be nested")
                else:
                    queued.append(line)
                    out.append("QUEUED")
            elif name == "MULTI":
                in_multi = True
                out.append("OK")
            else:
                out.extend(self.reply(line))
        return docs_sync.SessionRun("\n".join(out) + "\n", stderr, 0, False)

    def reply(self, line: str) -> list[str]:
        argv = line.split()
        name = argv[0].upper()
        if name == "FLUSHALL":
            if self.flush_reply != "OK":
                return [self.flush_reply]
            self.store.clear()
            return ["OK"]
        if name == "ACL" and argv[1].upper() == "SETUSER":
            self.users.append(argv[2])
            return ["OK"]
        if name == "ACL" and argv[1].upper() == "USERS":
            return [f'{i}) "{user}"' for i, user in enumerate(self.users, 1)] or ["(empty array)"]
        if name == "SET":
            self.store[argv[1]] = argv[2]
            return ["OK"]
        if name == "GET":
            value = self.store.get(argv[1])
            return [f'"{value}"' if value is not None else "(nil)"]
        if name == "LRANGE":
            return ['1) "a"', '2) "b"']
        if name == "BOOM":
            return ["(error) ERR boom"]
        if name == "EXEC":
            return ["(error) ERR EXEC without MULTI"]
        raise AssertionError(f"unexpected command in session: {line}")

    def exec(self, argv: list[str]) -> tuple[str, str, int | None]:
        self.calls.append(argv)
        return " ".join(argv), "", 0


def plan_and_split(commands: list[str], stdout_lines: list[str]) -> docs_sync.SessionSplit:
    plan = docs_sync.plan_session(commands, flush=False)
    return docs_sync.split_session_output("\n".join(stdout_lines) + "\n", plan)


class SessionSplitterTests(unittest.TestCase):
    def test_plain_replies(self) -> None:
        split = plan_and_split(["SET k v", "GET k"],
                               ["OK", marker_reply(0), '"v"', marker_reply(1)])
        self.assertIsNone(split.failure)
        self.assertEqual(split.outputs, ["OK", '"v"'])

    def test_multi_line_replies(self) -> None:
        split = plan_and_split(
            ["LRANGE l 0 -1", "HELLO 3"],
            ['1) "a"', '2) "b"', marker_reply(0),
             '1# "server" => "redis"', '2# "proto" => (integer) 3', marker_reply(1)])
        self.assertIsNone(split.failure)
        self.assertEqual(split.outputs, ['1) "a"\n2) "b"',
                                         '1# "server" => "redis"\n2# "proto" => (integer) 3'])

    def test_error_replies_are_kept_and_detected(self) -> None:
        split = plan_and_split(["SELECT 0", "GET"], [
            "(error) NOPERM bob has no ACL permissions", marker_reply(0),
            "(error) ERR wrong number of arguments for 'get' command", marker_reply(1)])
        self.assertIsNone(split.failure)
        self.assertEqual(docs_sync.error_reply(split.outputs[0]),
                         "(error) NOPERM bob has no ACL permissions")
        self.assertEqual(docs_sync.error_reply("1) OK\n2) (error) WRONGTYPE Operation"),
                         "2) (error) WRONGTYPE Operation")
        self.assertEqual(docs_sync.error_reply("Invalid argument(s)"), "Invalid argument(s)")
        self.assertIsNone(docs_sync.error_reply('"(error) is just a string here"'))

    def test_multi_queued_exec(self) -> None:
        commands = ["MULTI", "SET a 1", "INCR", "EXEC", "GET a"]
        plan = docs_sync.plan_session(commands, flush=True)
        # No marker between MULTI and EXEC: an unknown command there would abort it.
        self.assertEqual(plan.script(), "FLUSHALL\n__DOCSYNC_SEP_0__\nMULTI\nSET a 1\nINCR\n"
                                        "EXEC\n__DOCSYNC_SEP_1__\nGET a\n__DOCSYNC_SEP_2__\n")
        split = docs_sync.split_session_output("\n".join([
            "OK", marker_reply(0), "OK", "QUEUED",
            "(error) ERR wrong number of arguments for 'incr' command",
            "(error) EXECABORT Transaction discarded because of previous errors",
            marker_reply(1), "(nil)", marker_reply(2)]) + "\n", plan)
        self.assertIsNone(split.failure)
        self.assertEqual(split.outputs, [
            "OK", "OK", "QUEUED", "(error) ERR wrong number of arguments for 'incr' command",
            "(error) EXECABORT Transaction discarded because of previous errors", "(nil)"])

    def test_reset_ends_multi_and_a_block_may_end_inside_multi(self) -> None:
        split = plan_and_split(["MULTI", "SET key value", "RESET", "EXEC"],
                               ["OK", "QUEUED", "RESET", marker_reply(0),
                                "(error) ERR EXEC without MULTI", marker_reply(1)])
        self.assertIsNone(split.failure)
        self.assertEqual(split.outputs[2:], ["RESET", "(error) ERR EXEC without MULTI"])

        plan = docs_sync.plan_session(["MULTI", "SET a 1"], flush=False)
        self.assertEqual(plan.script(), "MULTI\nSET a 1\n__DOCSYNC_SEP_0__\n")
        split = docs_sync.split_session_output(
            "OK\nQUEUED\n" + marker_reply(0) + "\n", plan)
        self.assertIsNone(split.failure)
        self.assertEqual(split.outputs, ["OK", "QUEUED"])

    def test_refused_multi_cannot_be_split(self) -> None:
        split = plan_and_split(["MULTI", "LRANGE l 0 -1", "EXEC"], [
            "(error) NOPERM user has no ACL permissions", '1) "a"', '2) "b"',
            "(error) ERR EXEC without MULTI", marker_reply(0)])
        self.assertEqual(split.failed_step, 0)
        self.assertIn("not OK", split.failure)

    def test_missing_marker(self) -> None:
        split = plan_and_split(["HELLO 3", "SET k v", "GET k"],
                               ['1# "server" => "redis"', marker_reply(0)])
        self.assertEqual(split.outputs, ['1# "server" => "redis"'])
        self.assertEqual(split.failed_step, 1)
        self.assertIn("no reply marker after `SET k v`", split.failure)

    def test_marker_out_of_order_and_trailing_output_fail(self) -> None:
        split = plan_and_split(["PING", "PING"], ["PONG", marker_reply(1), "PONG", marker_reply(0)])
        self.assertEqual(split.failed_step, 0)
        split = plan_and_split(["PING"], ["PONG", marker_reply(0), "stray"])
        self.assertIn("unexpected output", split.failure)

    def test_slow_command_timing_line_is_dropped(self) -> None:
        split = plan_and_split(["BLPOP empty 1"], ["(nil)", "(1.00s)", marker_reply(0)])
        self.assertEqual(split.outputs, ["(nil)"])

    def test_marker_reply_with_redis_style_suffix_is_recognised(self) -> None:
        split = plan_and_split(["PING"], [
            "PONG", "(error) ERR unknown command '__docsync_sep_0__', with args beginning with: "])
        self.assertIsNone(split.failure)


class SessionExampleTests(unittest.TestCase):
    def test_rewritten_block_keeps_the_blank_line_after_it(self) -> None:
        markdown = "Intro.\n\n```shell\ndragonfly> GET key\n(nil)\n```\n\nAfter the block.\n"

        updated, _errors, _notes = docs_sync.verify_and_substitute_examples(
            markdown, FakeDockerSession(),
        )

        self.assertTrue(updated.endswith("(nil)\n```\n\nAfter the block.\n"))

    def test_regular_block_runs_in_one_session(self) -> None:
        session = FakeDockerSession()
        markdown = """\
```shell
dragonfly> SET key value
predicted
dragonfly> GET key
predicted
```
"""

        updated, errors, notes = docs_sync.verify_and_substitute_examples(markdown, session)

        self.assertEqual(errors, [])
        self.assertEqual(session.scripts, [
            "FLUSHALL\n__DOCSYNC_SEP_0__\nSET key value\n__DOCSYNC_SEP_1__\n"
            "GET key\n__DOCSYNC_SEP_2__\n"])
        self.assertIn('dragonfly> SET key value\nOK\ndragonfly> GET key\n"value"\n```', updated)
        self.assertTrue(any("one redis-cli session per block" in note for note in notes))

    def test_command_lines_are_sent_verbatim(self) -> None:
        # redis-cli parses quotes and \\x escapes itself; the harness must not.
        session = FakeDockerSession()
        markdown = '```shell\ndragonfly> SET k "a\\x41 b"   \n```\n'
        docs_sync.verify_and_substitute_examples(markdown, session)
        self.assertIn('\nSET k "a\\x41 b"\n__DOCSYNC_SEP_1__\n', session.scripts[0])

    def test_transaction_block_keeps_connection_state(self) -> None:
        session = FakeDockerSession()
        markdown = """\
```shell
dragonfly> MULTI
OK
dragonfly> SET a 1
QUEUED
dragonfly> GET a
QUEUED
dragonfly> EXEC
1) OK
dragonfly> GET a
"0"
```
"""

        updated, errors, _notes = docs_sync.verify_and_substitute_examples(markdown, session)

        self.assertEqual(errors, [])
        self.assertIn('dragonfly> EXEC\n1) OK\n2) "1"\ndragonfly> GET a\n"1"\n```', updated)

    def test_error_replies_are_recorded_and_written(self) -> None:
        markdown = "```shell\ndragonfly> SET k v\nOK\ndragonfly> BOOM\nOK\n```\n"

        updated, errors, notes = docs_sync.verify_and_substitute_examples(
            markdown, FakeDockerSession())

        self.assertEqual(errors, [{"block": 1, "command": "BOOM", "reply": "(error) ERR boom"}])
        self.assertIn("dragonfly> BOOM\n(error) ERR boom\n```", updated)
        self.assertTrue(any("1 error repl(ies)" in note for note in notes))

    def test_block_that_times_out_raises_naming_the_block(self) -> None:
        markdown = ("```shell\ndragonfly> GET key\n(nil)\n```\n\n"
                    "```shell\ndragonfly> SET key value\ndragonfly> BLPOP empty 0\n```\n")
        with self.assertRaises(docs_sync.ExampleRunError) as raised:
            docs_sync.verify_and_substitute_examples(
                markdown, FakeDockerSession(timeout_on="BLPOP empty 0"))
        message = str(raised.exception)
        self.assertIn("shell block 2 (line 6", message)
        self.assertIn("`BLPOP empty 0` did not return", message)

    def test_changed_regular_block_is_verified_with_production_baseline(self) -> None:
        session = FakeDockerSession()
        baseline = "```shell\ndragonfly> GET key\nold output\n```\n"
        changed = baseline.replace("old output", "new prediction")

        updated, errors, _notes = docs_sync.verify_and_substitute_examples(
            changed, session, baseline_text=baseline,
        )

        self.assertEqual(errors, [])
        self.assertEqual(len(session.scripts), 1)
        self.assertIn("dragonfly> GET key\n(nil)", updated)

    def test_unchanged_block_does_not_churn_dynamic_output(self) -> None:
        session = FakeDockerSession()
        markdown = "```shell\ndragonfly> GET key\ncurated dynamic output\n```\n"

        updated, errors, notes = docs_sync.verify_and_substitute_examples(
            markdown, session, baseline_text=markdown,
        )

        self.assertEqual(updated, markdown)
        self.assertEqual(errors, [])
        self.assertEqual(session.scripts, [])
        self.assertTrue(any("dynamic-output churn" in note for note in notes))


class FixedSession:
    """Answers every session with one canned redis-cli run."""

    def __init__(self, run: docs_sync.SessionRun) -> None:
        self.run = run

    def run_session(self, _script: str) -> docs_sync.SessionRun:
        return self.run


class UntrustedBlockTests(unittest.TestCase):
    """A block whose replies all arrived can still be wrong; such a block
    fails like one that did not complete."""

    def test_refused_flushall_fails_the_block(self) -> None:
        # An earlier example set requirepass: every reply would be NOAUTH.
        session = FakeDockerSession(flush_reply="(error) NOAUTH Authentication required.")

        block_run = docs_sync.run_example_block(session, ["GET k"])

        self.assertEqual(block_run.outputs, [])
        self.assertIn("FLUSHALL before the block replied", block_run.failure)
        with self.assertRaises(docs_sync.ExampleRunError):
            docs_sync.verify_and_substitute_examples(
                "```shell\ndragonfly> GET k\n(nil)\n```\n", session)
        observations, notes = docs_sync.observe_examples(
            session, "```shell\ndragonfly> GET k\n```\n")
        self.assertTrue(observations[0]["not_run"])
        self.assertTrue(any("did not complete: block 1: FLUSHALL" in n for n in notes))

    def test_lost_connection_fails_the_block(self) -> None:
        # CLIENT KILL of redis-cli's own address: its reply never comes,
        # redis-cli reconnects and runs the rest without the block's state.
        kill = "CLIENT KILL LADDR 127.0.0.1:6379"
        page = f"```shell\ndragonfly> SET k v\nOK\ndragonfly> {kill}\n(integer) 1\n```\n"

        observations, _notes = docs_sync.observe_examples(
            FakeDockerSession(drop_connection_on=kill), page)
        self.assertEqual([o.get("not_run") for o in observations], [True, True])

        with self.assertRaises(docs_sync.ExampleRunError) as raised:
            docs_sync.verify_and_substitute_examples(
                page, FakeDockerSession(drop_connection_on=kill))
        self.assertIn("connection error", str(raised.exception))
        self.assertIn("Server closed the connection", str(raised.exception))

    def test_non_zero_exit_fails_the_block(self) -> None:
        stdout = "\n".join(["OK", marker_reply(0), "PONG", marker_reply(1)]) + "\n"
        block_run = docs_sync.run_example_block(
            FixedSession(docs_sync.SessionRun(stdout, "", 1, False)), ["PING"])
        self.assertEqual(block_run.outputs, [])
        self.assertIn("exited with status 1", block_run.failure)

    def test_quit_is_explained(self) -> None:
        # redis-cli exits on QUIT without sending it: the marker never comes.
        stdout = "\n".join(["OK", marker_reply(0), "PONG", marker_reply(1)]) + "\n"
        block_run = docs_sync.run_example_block(
            FixedSession(docs_sync.SessionRun(stdout, "", 0, False)), ["PING", "QUIT"])
        self.assertEqual(block_run.outputs, ["PONG"])
        self.assertIn("no reply marker after `QUIT`", block_run.failure)
        self.assertIn("exits on QUIT and EXIT", block_run.failure)

    def test_replies_before_a_timeout_are_kept(self) -> None:
        block_run = docs_sync.run_example_block(
            FakeDockerSession(timeout_on="BLPOP empty 0"), ["SET k v", "BLPOP empty 0"])
        self.assertEqual(block_run.outputs, ["OK"])


class ReplayTests(unittest.TestCase):
    BASELINE = ("```shell\ndragonfly> ACL SETUSER alice\nOK\n```\n\n"
                "```shell\ndragonfly> ACL USERS\n1) \"alice\"\n```\n\n"
                "```shell\ndragonfly> ACL SETUSER bob\nOK\n```\n")

    def test_changed_block_sees_server_state_of_earlier_blocks_only(self) -> None:
        session = FakeDockerSession()
        changed = self.BASELINE.replace('1) "alice"', "predicted")

        updated, errors, notes = docs_sync.verify_and_substitute_examples(
            changed, session, baseline_text=self.BASELINE)

        self.assertEqual(errors, [])
        # Block 1 is replayed for the user it creates, block 2 is verified,
        # block 3 comes after the last changed block and is not run.
        self.assertEqual(len(session.scripts), 2)
        self.assertIn("ACL SETUSER alice", session.scripts[0])
        self.assertEqual(updated, self.BASELINE)
        self.assertEqual(session.users, ["alice"])
        self.assertTrue(any("replayed 1 unchanged block(s)" in n for n in notes))

    def test_replayed_block_that_does_not_complete_does_not_fail_the_page(self) -> None:
        session = FakeDockerSession(timeout_on="BLPOP empty 0")
        baseline = ("```shell\ndragonfly> BLPOP empty 0\n(nil)\n```\n\n"
                    "```shell\ndragonfly> GET a\n(nil)\n```\n")
        changed = baseline.replace("GET a\n(nil)", "GET a\npredicted")

        updated, _errors, notes = docs_sync.verify_and_substitute_examples(
            changed, session, baseline_text=baseline)

        self.assertEqual(updated, baseline)
        self.assertTrue(any("did not complete (their text is kept): block 1" in n
                            for n in notes), notes)

    def test_no_changed_block_runs_nothing(self) -> None:
        session = FakeDockerSession()
        docs_sync.verify_and_substitute_examples(self.BASELINE, session,
                                                 baseline_text=self.BASELINE)
        self.assertEqual(session.scripts, [])


class KeptLinesTests(unittest.TestCase):
    def test_blank_and_comment_lines_between_commands_are_kept(self) -> None:
        markdown = ("```shell\n# Set it.\ndragonfly> SET k v\npredicted\n\n# Read it back.\n"
                    "dragonfly> GET k\npredicted\n\ndragonfly> GET k\n# done\n```\n")

        updated, _errors, _notes = docs_sync.verify_and_substitute_examples(
            markdown, FakeDockerSession())

        self.assertEqual(updated, "```shell\n# Set it.\ndragonfly> SET k v\nOK\n\n"
                                  "# Read it back.\ndragonfly> GET k\n\"v\"\n\n"
                                  "dragonfly> GET k\n\"v\"\n# done\n```\n")

    def test_info_section_header_is_output_not_a_comment(self) -> None:
        kept = docs_sync.kept_separator_lines
        self.assertEqual(kept(["# Keyspace", ""], ["# Keyspace"]), [""])
        self.assertEqual(kept(["# Memory", "used_memory:1", ""],
                              ["# Memory", "used_memory:2"]), [""])
        self.assertEqual(kept(["OK", "", "# next step"], ["OK"]), ["", "# next step"])
        self.assertEqual(kept(["predicted"], ["OK"]), [])


class SkippedBlockTests(unittest.TestCase):
    def test_wait_block_is_preserved_verbatim(self) -> None:
        session = FakeDockerSession()
        markdown = """\
```shell
dragonfly> SET foo bar
OK
dragonfly> WAIT 1 100
(integer) 1
```
"""

        updated, errors, notes = docs_sync.verify_and_substitute_examples(markdown, session)

        self.assertEqual(updated, markdown)
        self.assertEqual(errors, [])
        self.assertEqual(session.scripts, [])
        self.assertTrue(any("topology-dependent" in note for note in notes))

    def test_push_mode_block_is_preserved_verbatim(self) -> None:
        for command in ("SUBSCRIBE news", "psubscribe news.*", "SSUBSCRIBE orders", "MONITOR"):
            with self.subTest(command=command):
                session = FakeDockerSession()
                markdown = f"```shell\ndragonfly> {command}\nReading messages...\n```\n"

                updated, errors, notes = docs_sync.verify_and_substitute_examples(
                    markdown, session)

                self.assertEqual(updated, markdown)
                self.assertEqual(session.scripts, [])
                self.assertTrue(any("push-mode" in note for note in notes))
        self.assertIsNone(docs_sync.topology_skip_reason("SUBSCRIBE news"))
        self.assertEqual(docs_sync.block_skip(["SET a 1", "SUBSCRIBE news"])[0], "push-mode")
        self.assertEqual(docs_sync.block_skip(["MONITOR", "WAIT 1 0"])[0], "topology")
        self.assertEqual(docs_sync.block_skip(["-p 6380 monitor"])[0], "push-mode")
        self.assertIsNone(docs_sync.block_skip(["UNSUBSCRIBE", "PUBLISH ch hi"]))

    def test_current_examples_are_observed_per_block(self) -> None:
        session = FakeDockerSession()
        page = ("```shell\ndragonfly> SET key value\nOK\ndragonfly> WAIT 1 100\n```\n\n"
                "```shell\ndragonfly> SUBSCRIBE ch\n```\n\n"
                "```shell\ndragonfly> SET key value\nOK\ndragonfly> BOOM\n```\n\n"
                "```shell\n$ redis-cli -p 6380 GET key\n```\n")

        observations, notes = docs_sync.observe_examples(session, page)

        self.assertEqual([o.get("skipped", False) for o in observations],
                         [True, True, True, False, False, False])
        self.assertIn("replication", observations[0]["skip_reason"])
        self.assertIn("push mode", observations[2]["skip_reason"])
        self.assertEqual(observations[4], {"block": 3, "invocation": "BOOM",
                                           "output": "(error) ERR boom", "error_reply": True})
        self.assertEqual(observations[5]["invocation"], "$ redis-cli -p 6380 GET key")
        self.assertEqual(session.calls, [["-p", "6380", "GET", "key"]])
        self.assertEqual(len(session.scripts), 1)
        self.assertTrue(any("1 error repl(ies)" in note for note in notes))

    def test_observation_records_a_block_that_did_not_complete(self) -> None:
        session = FakeDockerSession(timeout_on="BLPOP empty 0")
        page = ("```shell\ndragonfly> SET k v\ndragonfly> BLPOP empty 0\ndragonfly> GET k\n```\n\n"
                "```shell\ndragonfly> GET k\n```\n")

        observations, notes = docs_sync.observe_examples(session, page)

        self.assertEqual(observations[0]["output"], "OK")
        self.assertTrue(observations[1]["not_run"])
        self.assertIn("`BLPOP empty 0` did not return", observations[1]["failure"])
        self.assertTrue(observations[2]["not_run"])
        self.assertEqual(observations[3], {"block": 2, "invocation": "GET k", "output": "(nil)",
                                           "error_reply": False})
        self.assertTrue(any("did not complete: block 1" in note for note in notes))

    def test_info_replication_is_topology_dependent(self) -> None:
        self.assertIsNotNone(docs_sync.topology_skip_reason("INFO replication"))
        self.assertIsNotNone(docs_sync.topology_skip_reason("INFO"))
        self.assertIsNotNone(docs_sync.topology_skip_reason("INFO default"))
        self.assertIsNone(docs_sync.topology_skip_reason("INFO memory"))

    def test_redis_cli_options_do_not_hide_topology_command(self) -> None:
        self.assertIsNotNone(
            docs_sync.topology_skip_reason("-p 1111 DFLYCLUSTER SLOT-MIGRATION-STATUS")
        )
        self.assertIsNotNone(docs_sync.topology_skip_reason("--tls --user admin ROLE"))

    def test_additional_native_topology_commands_are_skipped(self) -> None:
        self.assertIsNotNone(docs_sync.topology_skip_reason("REPLTAKEOVER 5"))
        self.assertIsNotNone(docs_sync.topology_skip_reason("DFLYMIGRATE FLOW ..."))

    def test_deterministic_cluster_subcommands_remain_verifiable(self) -> None:
        self.assertIsNone(docs_sync.topology_skip_reason("CLUSTER KEYSLOT user:1"))
        self.assertIsNone(docs_sync.topology_skip_reason("CLUSTER HELP"))
        self.assertIsNotNone(docs_sync.topology_skip_reason("CLUSTER NODES"))


PAGE_HEAD = "---\ndescription: test page\n---\n# {title}\n\n"


class StructuralValidationTests(unittest.TestCase):
    def test_structural_validation_rejects_topology_output_rewrite(self) -> None:
        original = PAGE_HEAD.format(title="WAIT") + """\
## Examples

```shell
dragonfly> WAIT 1 100
(integer) 1
```
"""
        rewritten = original.replace("(integer) 1", "(integer) 0")

        errors = docs_sync.validate_update_output(original, rewritten)

        self.assertTrue(any("topology-dependent" in error for error in errors))

    def test_structural_validation_rejects_dflycluster_rewrite(self) -> None:
        original = PAGE_HEAD.format(title="DFLYCLUSTER SLOT-MIGRATION-STATUS") + """\
## Examples

```shell
dragonfly> DFLYCLUSTER SLOT-MIGRATION-STATUS
1) 1) "out"
```
"""
        rewritten = original.replace('1) 1) "out"', "(empty array)")

        errors = docs_sync.validate_update_output(original, rewritten)

        self.assertTrue(any("topology-dependent" in error for error in errors))

    def test_structural_validation_rejects_push_mode_rewrite(self) -> None:
        original = PAGE_HEAD.format(title="SUBSCRIBE") + """\
## Examples

```shell
dragonfly> SUBSCRIBE news
1) "subscribe"
2) "news"
3) (integer) 1
```
"""
        rewritten = original.replace("(integer) 1", "(integer) 2")

        errors = docs_sync.validate_update_output(original, rewritten)

        self.assertTrue(any("push-mode" in error for error in errors))
        self.assertEqual(docs_sync.validate_update_output(original, original), [])

    def acl_page(self, acl_line: str) -> str:
        return PAGE_HEAD.format(title="MEMORY DEFRAGMENT-SEGMENTS") + f"""\
## Syntax

    MEMORY DEFRAGMENT-SEGMENTS [threshold]

**Time complexity:** O(N)

{acl_line}

Relocates segments. This paragraph pads the page past the length checks.
"""

    def test_qualified_acl_line_is_guarded(self) -> None:
        original = self.acl_page("**ACL categories (Dragonfly v2.0.2):** @read, @slow")

        for changed in ("**ACL categories (Dragonfly v2.1.0):** @read, @slow",
                        "**ACL categories:** @admin, @dangerous, @slow",
                        "**ACL categories (Dragonfly v2.0.2):** @read, @slow, @admin"):
            with self.subTest(changed=changed):
                errors = docs_sync.validate_update_output(
                    original, self.acl_page(changed))
                self.assertTrue(any("modified or removed" in e for e in errors), errors)
        self.assertEqual(docs_sync.validate_update_output(original, original), [])
        # Trailing whitespace is cosmetic.
        self.assertEqual(docs_sync.validate_update_output(
            original, original.replace("@read, @slow", "@read, @slow  ")), [])

    def test_every_acl_line_is_guarded_and_none_may_be_added(self) -> None:
        original = self.acl_page("- **ACL categories:** @admin, @slow\n\n"
                                 "**ACL Category:** @dangerous")
        second_changed = original.replace("**ACL Category:** @dangerous",
                                          "**ACL Category:** @fast")
        errors = docs_sync.validate_update_output(original, second_changed)
        self.assertTrue(any("@dangerous" in e for e in errors), errors)

        no_line = self.acl_page("")
        added = no_line.replace("Relocates", "**ACL categories:** @read, @slow\n\nRelocates")
        errors = docs_sync.validate_update_output(no_line, added)
        self.assertTrue(any("was added" in e for e in errors), errors)

        duplicated = original.replace("Relocates", "**ACL Category:** @dangerous\n\nRelocates")
        errors = docs_sync.validate_update_output(original, duplicated)
        self.assertTrue(any("was added" in e for e in errors), errors)


V2_1_FACTS = {"data": {
    "commands": {"ACL": {"arity": -2}, "ACL SETUSER": {"arity": -3},
                 "CLIENT": {"arity": -2}, "MEMORY": {"arity": -2}, "CLUSTER": {"arity": -2}},
    # v2.1.0 ACL CAT spells subcommands with their own entry as CMD|SUB.
    "command_acl": {"ACL": ["@slow"], "ACL|SETUSER": ["@admin", "@dangerous", "@slow"],
                    "CLIENT": ["@connection", "@slow"],
                    "CLIENT|KILL": ["@admin", "@connection", "@dangerous", "@slow"],
                    "MEMORY": ["@read", "@slow"], "CLUSTER": ["@slow"]},
}}


class AclCategoriesTests(unittest.TestCase):
    def test_lookup_follows_acl_model(self) -> None:
        cases = {
            ("docs/command-reference/acl/setuser.md", "ACL SETUSER"):
                ["@admin", "@dangerous", "@slow"],
            ("docs/command-reference/server-management/client-kill.md", "CLIENT KILL"):
                ["@admin", "@connection", "@dangerous", "@slow"],
            ("docs/command-reference/server-management/memory-usage.md", "MEMORY USAGE"):
                ["@read", "@slow"],
        }
        for (rel, command), expected in cases.items():
            with self.subTest(command=command):
                self.assertIsNone(V2_1_FACTS["data"]["command_acl"].get(command))
                self.assertEqual(docs_sync.page_acl_categories(rel, command, V2_1_FACTS),
                                 expected)

    def test_pages_outside_the_command_reference_get_no_categories(self) -> None:
        self.assertEqual(docs_sync.page_acl_categories(
            "docs/managing-dragonfly/cluster-mode.md", "CLUSTER MODE", V2_1_FACTS), [])
        self.assertEqual(docs_sync.page_acl_categories(
            "docs/command-reference/acl/setuser.md", None, V2_1_FACTS), [])
        self.assertEqual(docs_sync.page_acl_categories(
            "docs/command-reference/x.md", "NOSUCH", V2_1_FACTS), [])


class DockerTimeoutTests(unittest.TestCase):
    def test_session_command_runs_under_timeout_in_the_container(self) -> None:
        session = docs_sync.DockerSession(container="c1", tag="v2.1.0")
        completed = subprocess.CompletedProcess([], 0, b"PONG\r\n", b"")
        with patch.object(docs_sync.subprocess, "run", return_value=completed) as run:
            result = session.run_session("PING\n")
        argv = run.call_args.args[0]
        self.assertEqual(argv, ["docker", "exec", "-i", "c1", "timeout", "-k", "5", "30",
                                "redis-cli", "--no-raw"])
        self.assertEqual(run.call_args.kwargs["input"], b"PING\n")
        self.assertGreater(run.call_args.kwargs["timeout"], 30)
        self.assertEqual((result.stdout, result.timed_out), ("PONG\n", False))

    def test_in_container_timeout_is_reported(self) -> None:
        session = docs_sync.DockerSession(container="c1", tag="v2.1.0")
        completed = subprocess.CompletedProcess([], 124, b"", b"")
        with patch.object(docs_sync.subprocess, "run", return_value=completed):
            self.assertTrue(session.run_session("BLPOP l 0\n").timed_out)
            stdout, stderr, rc = session.exec(["BLPOP", "l", "0"])
        self.assertIsNone(rc)
        self.assertIn("timed out after 30 s", stderr)

    def test_host_side_timeout_raises(self) -> None:
        session = docs_sync.DockerSession(container="c1", tag="v2.1.0")
        expired = subprocess.TimeoutExpired(["docker"], 50, output=b"partial")
        with patch.object(docs_sync.subprocess, "run", side_effect=expired):
            with self.assertRaises(docs_sync.DockerTimeout):
                session.run_session("PING\n")
            with self.assertRaises(docs_sync.DockerTimeout):
                session.exec(["PING"])

    def test_boot_reports_an_image_without_timeout(self) -> None:
        missing = subprocess.CompletedProcess([], 126, "", 'exec: "timeout": not found')
        removed: list[str] = []
        with patch.multiple(docs_sync,
                            run=lambda cmd, **_k: missing if cmd[1] == "exec" else None,
                            remove_container=removed.append):
            with self.assertRaises(RuntimeError) as raised:
                docs_sync.boot_docker("v2.1.0")
        self.assertIn("cannot run `timeout ... redis-cli`", str(raised.exception))
        self.assertEqual(len(removed), 1)

    def test_boot_survives_a_hung_ping(self) -> None:
        calls: list[list[str]] = []

        def fake_run(cmd, **_kwargs):
            calls.append(cmd)
            if cmd[1] == "exec" and len(calls) == 2:
                raise subprocess.TimeoutExpired(cmd, 20)
            return subprocess.CompletedProcess(cmd, 0, "PONG\n", "")

        with patch.object(docs_sync, "run", side_effect=fake_run):
            session = docs_sync.boot_docker("v2.1.0")
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[1][3:6], ["timeout", "5", "redis-cli"])
        self.assertTrue(session.container.startswith("dfly-docs-sync-v2-1-0-"))


class FakeClient:
    def close(self) -> None:
        pass


class UpdateOneFileTests(unittest.TestCase):
    def run_update(self, page: str, llm_markdown: str, session: FakeDockerSession,
                   rel: str = "docs/command-reference/acl/setuser.md",
                   boot=None, kill=None):
        prompts: list[str] = []

        def fake_llm(_client, _system, user_text, *_args):
            prompts.append(user_text)
            return ({"markdown": llm_markdown, "notes": []},
                    {"input_tokens": 1, "output_tokens": 1, "reasoning_tokens": 0})

        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            path = root / rel
            path.parent.mkdir(parents=True)
            path.write_text(page)
            with (
                patch.multiple(
                    docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs",
                    LLM_DEBUG_DIR=root / "llm_debug",
                    boot_docker=boot or (lambda *_a, **_k: session),
                    kill_docker=kill or (lambda _s: None),
                    create_client=FakeClient,
                    call_llm_streaming=fake_llm,
                    find_command_handler_source=lambda *_a: None,
                    pick_sibling_style_reference=lambda _rel: None,
                ),
                patch.dict(docs_sync.os.environ, {"OPENAI_API_KEY": "test"}),
                redirect_stdout(io.StringIO()),
            ):
                result = docs_sync.update_one_file({"path": rel}, "v2.1.0", V2_1_FACTS,
                                                   root, dry_run=False)
            written = path.read_text()
            debug = sorted((root / "llm_debug").glob("*.md")) if (root / "llm_debug").exists() else []
        return result, written, prompts, debug

    PAGE = PAGE_HEAD.format(title="ACL SETUSER") + """\
## Examples

**ACL categories:** @admin, @dangerous, @slow

Padding text that keeps the page well above the structural length checks.

```shell
dragonfly> GET key
(nil)
```
"""

    def test_block_that_does_not_complete_fails_the_page(self) -> None:
        llm = self.PAGE.replace("(nil)\n```", "(nil)\ndragonfly> BLPOP empty 0\n(nil)\n```")
        result, written, prompts, debug = self.run_update(
            self.PAGE, llm, FakeDockerSession(timeout_on="BLPOP empty 0"))

        self.assertEqual(result["status"], "failed")
        self.assertIn("shell block 1", result["error"])
        self.assertIn("`BLPOP empty 0` did not return", result["error"])
        self.assertEqual(written, self.PAGE)
        self.assertEqual(len(debug), 1)
        self.assertIn("@admin, @dangerous, @slow", prompts[0].split("=== acl_categories")[1])

    def test_error_replies_are_listed_in_the_result(self) -> None:
        llm = self.PAGE.replace("(nil)\n```", "(nil)\ndragonfly> BOOM\nOK\n```")
        result, written, _prompts, _debug = self.run_update(self.PAGE, llm, FakeDockerSession())

        self.assertEqual(result["status"], "updated")
        self.assertEqual(result["example_errors"],
                         [{"block": 1, "command": "BOOM", "reply": "(error) ERR boom"}])
        self.assertIn("dragonfly> BOOM\n(error) ERR boom\n```", written)

    def booting(self, sessions: list[FakeDockerSession], fail_on: int | None = None):
        booted: list[FakeDockerSession] = []
        killed: list[FakeDockerSession] = []

        def boot(*_args, **_kwargs):
            if len(booted) == fail_on:
                raise RuntimeError("Dragonfly v2.1.0 did not respond to PING")
            booted.append(sessions[len(booted)])
            return booted[-1]

        return booted, killed, boot, killed.append

    def test_changed_block_is_verified_on_a_fresh_container(self) -> None:
        # The pre-LLM pass leaves ACL users behind; the changed block must not see them.
        page = self.PAGE.replace("dragonfly> GET key\n(nil)",
                                 "dragonfly> ACL SETUSER alice\nOK\ndragonfly> ACL USERS\n"
                                 '1) "alice"')
        llm = page.replace('1) "alice"', '1) "alice"\n2) "predicted"')
        sessions = [FakeDockerSession(), FakeDockerSession()]
        booted, killed, boot, kill = self.booting(sessions)

        result, written, _prompts, _debug = self.run_update(
            page, llm, sessions[0], boot=boot, kill=kill)

        self.assertEqual(result["status"], "unchanged", result)
        self.assertEqual(booted, sessions)
        self.assertEqual(killed, sessions)
        self.assertEqual(len(sessions[0].scripts), 1)  # the pre-LLM pass
        self.assertEqual(len(sessions[1].scripts), 1)  # the changed block, on its own
        self.assertEqual(sessions[1].users, ["alice"])
        self.assertEqual(written, page)

    def test_unchanged_examples_need_no_second_container(self) -> None:
        sessions = [FakeDockerSession(), FakeDockerSession()]
        booted, killed, boot, kill = self.booting(sessions)
        llm = self.PAGE.replace("Padding text", "Changed padding text")

        result, written, _prompts, _debug = self.run_update(
            self.PAGE, llm, sessions[0], boot=boot, kill=kill)

        self.assertEqual(result["status"], "updated")
        self.assertEqual(booted, sessions[:1])
        self.assertEqual(killed, sessions[:1])
        self.assertEqual(written, llm)

    def test_second_container_that_does_not_boot_fails_the_page(self) -> None:
        sessions = [FakeDockerSession(), FakeDockerSession()]
        booted, killed, boot, kill = self.booting(sessions, fail_on=1)
        llm = self.PAGE.replace("(nil)\n```", "(nil)\ndragonfly> GET key\n(nil)\n```")

        result, written, _prompts, debug = self.run_update(
            self.PAGE, llm, sessions[0], boot=boot, kill=kill)

        self.assertEqual(result["status"], "failed")
        self.assertIn("docker boot for example verification failed", result["error"])
        self.assertEqual(written, self.PAGE)
        self.assertEqual(len(debug), 1)
        self.assertEqual(killed, sessions[:1])

    def test_examples_added_to_a_page_without_examples_are_verified(self) -> None:
        page = PAGE_HEAD.format(title="Running in containers") + (
            "## Usage\n\nPadding text that keeps the page well above the structural "
            "length checks of the validator.\n")
        llm = page + "\n```shell\ndragonfly> SET k v\npredicted\n```\n"
        session = FakeDockerSession()
        booted, killed, boot, kill = self.booting([session])

        result, written, _prompts, _debug = self.run_update(
            page, llm, session, rel="docs/managing-dragonfly/containers.md",
            boot=boot, kill=kill)

        self.assertEqual(result["status"], "updated")
        self.assertEqual(booted, [session])
        self.assertEqual(killed, [session])
        self.assertTrue(written.endswith("dragonfly> SET k v\nOK\n```\n"))

    def test_new_push_mode_block_is_reported_as_unverified(self) -> None:
        llm = self.PAGE + '\n```shell\ndragonfly> SUBSCRIBE news\n1) "subscribe"\n```\n'

        result, written, _prompts, _debug = self.run_update(self.PAGE, llm, FakeDockerSession())

        self.assertEqual(result["status"], "updated")
        self.assertEqual(result["unverified_blocks"],
                         [{"block": 2, "kind": "push-mode", "command": "SUBSCRIBE news"}])
        self.assertTrue(any("LLM's prediction" in note for note in result["notes"]))
        self.assertEqual(written, llm)
        self.assertEqual(docs_sync.unverified_new_blocks(self.PAGE, self.PAGE), [])

    def test_new_redis_cli_block_is_kept_and_reported_as_unverified(self) -> None:
        llm = self.PAGE + "\n```shell\n$ redis-cli -3 HELLO\npredicted\n```\n"
        session = FakeDockerSession()

        result, written, _prompts, _debug = self.run_update(self.PAGE, llm, session)

        self.assertEqual(result["status"], "updated")
        self.assertEqual(result["unverified_blocks"],
                         [{"block": 2, "kind": "redis-cli", "command": "$ redis-cli -3 HELLO"}])
        self.assertTrue(any("`$ redis-cli` lines as written" in note for note in result["notes"]))
        self.assertEqual(written, llm)
        self.assertEqual(session.calls, [])


class SummaryTests(unittest.TestCase):
    def test_summary_lists_error_replies_and_unverified_blocks(self) -> None:
        results = [{"path": "docs/command-reference/x.md", "status": "updated", "notes": [],
                    "example_errors": [{"block": 1, "command": "BOOM",
                                        "reply": "(error) ERR boom"}],
                    "unverified_blocks": [{"block": 2, "kind": "push-mode",
                                           "command": "SUBSCRIBE news"}]}]
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            plan = root / "plan.json"
            plan.write_text('{"after": "v2.1.0", "files_to_update": []}')
            out = io.StringIO()
            with (
                patch.multiple(docs_sync, REPO_ROOT=root, PLANS_DIR=root / "plans",
                               update_phase=lambda *_a, **_k: results),
                patch.object(docs_sync.sys, "argv",
                             ["docs_sync.py", "--update-only-from", str(plan)]),
                redirect_stdout(out),
            ):
                code = docs_sync.main()
        self.assertEqual(code, 0)
        self.assertIn("docs/command-reference/x.md (updated): block 1: BOOM -> "
                      "(error) ERR boom", out.getvalue())
        self.assertIn("New example blocks that were not run (1)", out.getvalue())
        self.assertIn("docs/command-reference/x.md (updated): block 2 (push-mode): "
                      "SUBSCRIBE news", out.getvalue())


class UnpublishedPageTests(unittest.TestCase):
    def test_unpublished_pages_are_neither_indexed_nor_planned(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            for rel in ("docs/command-reference/stream/xgroup.md",
                        "docs/command-reference/pubsub/_unsupported/xgroup.md",
                        "docs/command-reference/_draft.md"):
                path = root / rel
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# XGROUP\n\nContainer.\n")
            with (
                patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs"),
                redirect_stdout(io.StringIO()),
            ):
                indexed = [entry["path"] for entry in docs_sync.collect_md_index()]
                planned = docs_sync.plannable_path(
                    "docs/command-reference/pubsub/_unsupported/xgroup.md", "--also-update")
                kept = docs_sync.plannable_path("docs/command-reference/stream/xgroup.md", "--also-update")
        self.assertEqual(indexed, ["docs/command-reference/stream/xgroup.md"])
        self.assertIsNone(planned)
        self.assertEqual(kept, "docs/command-reference/stream/xgroup.md")


class ContentGuardTests(unittest.TestCase):
    PAGE = """---
description: "Offload large string values to SSD/NVMe storage."
---

import PageTitle from '@site/src/components/PageTitle';

# FT.ALIASDEL

<PageTitle title="Redis FT.ALIASDEL Command (Documentation) | Dragonfly" />

## Syntax

    FT.ALIASDEL alias

Batch I/O counters are available through `INFO stats`.
Padding text that keeps the page well above the structural length checks of the validator.

## Examples

```shell
dragonfly> FT.ALIASDEL products
OK
dragonfly> FT.SEARCH products-v2 * NOCONTENT
1) (integer) 1
2) "v2:1"
```

``` bash
dragonfly> FT.CREATE idx ON JSON SCHEMA $.title AS title TEXT
```
"""

    def test_changed_front_matter_is_rejected(self) -> None:
        out = self.PAGE.replace("SSD/NVMe", "SSD/NMe")
        self.assertIn("frontmatter was changed; it must stay byte-identical",
                      docs_sync.validate_update_output(self.PAGE, out))

    def test_removed_or_replaced_example_commands_are_rejected(self) -> None:
        out = self.PAGE.replace("dragonfly> FT.SEARCH products-v2 * NOCONTENT\n1) (integer) 1\n2) \"v2:1\"\n", "")
        out = out.replace("$.title AS title TEXT", "$.title AS title_text TEXT")
        errors = docs_sync.validate_update_output(self.PAGE, out)
        self.assertTrue(any(e.startswith("2 existing example command(s) were removed") for e in errors), errors)

    def test_changed_redis_cli_invocations_are_rejected(self) -> None:
        page = self.PAGE + "\n```shell\n$ redis-cli -3 HELLO\n```\n"
        out = page.replace("$ redis-cli -3 HELLO", "$ redis-cli -2 HELLO")
        errors = docs_sync.validate_update_output(page, out)
        self.assertTrue(any(e.startswith("1 existing example command(s) were removed") for e in errors), errors)

    def test_added_setup_lines_are_accepted(self) -> None:
        out = self.PAGE.replace("```shell\n", "```shell\ndragonfly> FT.CREATE products-v2 ON HASH PREFIX 1 v2: SCHEMA title TEXT\nOK\n", 1)
        self.assertEqual(docs_sync.validate_update_output(self.PAGE, out), [])

    def test_removed_prose_is_reported(self) -> None:
        out = self.PAGE.replace("Batch I/O counters are available through `INFO stats`.\n", "")
        self.assertEqual(docs_sync.removed_prose(self.PAGE, out),
                         ["Batch I/O counters are available through `INFO stats`."])
        self.assertEqual(docs_sync.removed_prose(self.PAGE, self.PAGE), [])


if __name__ == "__main__":
    unittest.main()
