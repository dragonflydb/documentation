from __future__ import annotations

import unittest

from tools.docsync import docs_sync


class FakeDockerSession:
    def __init__(self) -> None:
        self.calls: list[list[str]] = []

    def exec(self, argv: list[str]) -> tuple[str, str, int]:
        self.calls.append(argv)
        if argv == ["FLUSHALL"]:
            return "OK", "", 0
        if argv[:1] == ["SET"]:
            return "OK", "", 0
        if argv[:1] == ["GET"]:
            return '"value"', "", 0
        raise AssertionError(f"unexpected Docker command: {argv}")


class TopologyExampleTests(unittest.TestCase):
    def test_topology_commands_are_marked_unverified(self) -> None:
        session = FakeDockerSession()

        observations = docs_sync.verify_invocations(
            session,
            ["SET key value", "WAIT 1 100", "DFLYCLUSTER SLOT-MIGRATION-STATUS"],
        )

        self.assertEqual(session.calls, [["SET", "key", "value"]])
        self.assertTrue(observations[1]["skipped"])
        self.assertIn("replication", observations[1]["skip_reason"])
        self.assertTrue(observations[2]["skipped"])

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

        updated, errors, notes = docs_sync.verify_and_substitute_examples(
            markdown, session,
        )

        self.assertEqual(updated, markdown)
        self.assertEqual(errors, [])
        self.assertEqual(session.calls, [])
        self.assertTrue(any("topology-dependent" in note for note in notes))

    def test_regular_block_still_uses_runtime_output(self) -> None:
        session = FakeDockerSession()
        markdown = """\
```shell
dragonfly> SET key value
predicted
dragonfly> GET key
predicted
```
"""

        updated, errors, _notes = docs_sync.verify_and_substitute_examples(
            markdown, session,
        )

        self.assertEqual(errors, [])
        self.assertEqual(
            session.calls,
            [["FLUSHALL"], ["SET", "key", "value"], ["GET", "key"]],
        )
        self.assertIn("dragonfly> SET key value\nOK", updated)
        self.assertIn('dragonfly> GET key\n"value"', updated)

    def test_changed_regular_block_is_verified_with_production_baseline(self) -> None:
        session = FakeDockerSession()
        baseline = """\
```shell
dragonfly> GET key
old output
```
"""
        changed = baseline.replace("old output", "new prediction")

        updated, errors, _notes = docs_sync.verify_and_substitute_examples(
            changed, session, baseline_text=baseline,
        )

        self.assertEqual(errors, [])
        self.assertEqual(session.calls, [["FLUSHALL"], ["GET", "key"]])
        self.assertIn('dragonfly> GET key\n"value"', updated)

    def test_unchanged_block_does_not_churn_dynamic_output(self) -> None:
        session = FakeDockerSession()
        markdown = """\
```shell
dragonfly> GET key
curated dynamic output
```
"""

        updated, errors, notes = docs_sync.verify_and_substitute_examples(
            markdown, session, baseline_text=markdown,
        )

        self.assertEqual(updated, markdown)
        self.assertEqual(errors, [])
        self.assertEqual(session.calls, [])
        self.assertTrue(any("dynamic-output churn" in note for note in notes))

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

    def test_structural_validation_rejects_topology_output_rewrite(self) -> None:
        original = """\
---
description: test page
---
# WAIT

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
        original = """\
---
description: test page
---
# DFLYCLUSTER SLOT-MIGRATION-STATUS

## Examples

```shell
dragonfly> DFLYCLUSTER SLOT-MIGRATION-STATUS
1) 1) "out"
```
"""
        rewritten = original.replace('1) 1) "out"', "(empty array)")

        errors = docs_sync.validate_update_output(original, rewritten)

        self.assertTrue(any("topology-dependent" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
