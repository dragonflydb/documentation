from __future__ import annotations

import io
import json
import os
import subprocess
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.docsync import compat_sync


class CheckoutTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.root = Path(temporary_dir.name)
        self.source = self.root / "source"
        self.checkout = self.root / "checkout"
        self.source.mkdir()
        self.git(self.source, "init", "--quiet")
        self.git(self.source, "config", "user.name", "Docsync Test")
        self.git(self.source, "config", "user.email", "docsync@example.com")
        self.commit("one", "v1")
        with redirect_stdout(io.StringIO()):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v1", refresh=False,
            )

    @staticmethod
    def git(cwd: Path, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ["git", *args], cwd=cwd, capture_output=True, text=True, check=True,
        )

    def commit(self, content: str, tag: str) -> None:
        (self.source / "content.txt").write_text(content, encoding="utf-8")
        self.git(self.source, "add", "content.txt")
        self.git(self.source, "commit", "--quiet", "-m", content)
        self.git(self.source, "tag", tag)

    def test_missing_cached_tag_is_fetched_and_checked_out(self) -> None:
        self.commit("two", "v2")

        output = io.StringIO()
        with redirect_stdout(output):
            resolved = compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v2", refresh=False,
            )

        self.assertEqual(resolved, self.checkout)
        self.assertEqual(
            self.git(self.checkout, "describe", "--tags", "--exact-match").stdout.strip(),
            "v2",
        )
        self.assertIn("fetching tags", output.getvalue())

    def rev(self, cwd: Path, ref: str) -> str:
        return self.git(cwd, "rev-parse", f"{ref}^{{commit}}").stdout.strip()

    def move_v1_upstream(self) -> None:
        (self.source / "content.txt").write_text("moved", encoding="utf-8")
        self.git(self.source, "commit", "--quiet", "-am", "moved")
        self.git(self.source, "tag", "--force", "v1")

    def test_checkout_is_retried_after_partially_failed_fetch(self) -> None:
        self.commit("two", "v2")
        self.move_v1_upstream()
        # A stale lock makes the v1 update fail (fetch exits non-zero) while the
        # new v2 tag is still installed.
        (self.checkout / ".git" / "refs" / "tags" / "v1.lock").write_text("")

        with redirect_stdout(io.StringIO()):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v2", refresh=False,
            )

        self.assertEqual(self.rev(self.checkout, "HEAD"), self.rev(self.source, "v2"))

    def test_cached_tag_that_moved_upstream_is_refetched(self) -> None:
        self.move_v1_upstream()
        output = io.StringIO()
        with redirect_stdout(output):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v1", refresh=False,
            )
        self.assertEqual(self.rev(self.checkout, "HEAD"), self.rev(self.source, "v1"))
        self.assertIn("moved upstream", output.getvalue())

    def test_moved_tag_is_refetched_with_refresh(self) -> None:
        self.move_v1_upstream()
        with redirect_stdout(io.StringIO()):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v1", refresh=True,
            )
        self.assertEqual((self.checkout / "content.txt").read_text(), "moved")

    def test_cached_tag_deleted_upstream_is_an_error(self) -> None:
        self.git(self.source, "tag", "-d", "v1")
        with redirect_stdout(io.StringIO()), self.assertRaises(RuntimeError) as raised:
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v1", refresh=False,
            )
        self.assertIn("no longer exists upstream", str(raised.exception))

    def test_tag_that_became_a_branch_upstream_recovers_with_refresh(self) -> None:
        self.git(self.source, "tag", "-d", "v1")
        self.git(self.source, "branch", "v1")
        with redirect_stdout(io.StringIO()):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v1", refresh=True,
            )

    def test_revision_expressions_are_not_mistaken_for_tags(self) -> None:
        self.commit("two", "v2")
        with redirect_stdout(io.StringIO()):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v2", refresh=False,
            )
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v2~1", refresh=False,
            )
        self.assertEqual(self.rev(self.checkout, "HEAD"), self.rev(self.source, "v1"))

    def test_source_dir_tag_missing_upstream_is_rejected(self) -> None:
        with (
            patch.object(compat_sync.dfly_refs, "upstream_tag_lookup", return_value=(True, None)),
            redirect_stdout(io.StringIO()),
            self.assertRaises(RuntimeError) as raised,
        ):
            compat_sync.verify_source_dir_ref(self.checkout, "v1")
        self.assertIn("does not exist upstream", str(raised.exception))

    def test_source_dir_inside_another_repo_has_no_commit(self) -> None:
        nested = self.checkout / "unpacked"
        nested.mkdir()
        self.assertIsNone(compat_sync.source_dir_commit(nested))
        self.assertEqual(compat_sync.source_dir_commit(self.checkout), self.rev(self.checkout, "HEAD"))

    def test_missing_source_dir_is_a_checkout_error(self) -> None:
        args = SimpleNamespace(dragonfly_source_dir=self.root / "missing", dragonfly_ref="v1")
        with self.assertRaises(RuntimeError):
            compat_sync.resolve_dragonfly_source(args)

    def test_source_dir_at_another_commit_than_ref_is_rejected(self) -> None:
        self.commit("two", "v2")
        with redirect_stdout(io.StringIO()):
            compat_sync.ensure_checkout(
                "fixture", str(self.source), self.checkout, "v2", refresh=False,
            )
        with (
            patch.object(compat_sync.dfly_refs, "upstream_tag_lookup", return_value=(False, None)),
            redirect_stdout(io.StringIO()),
        ):
            compat_sync.verify_source_dir_ref(self.checkout, "v2")
            with self.assertRaises(RuntimeError) as raised:
                compat_sync.verify_source_dir_ref(self.checkout, "v1")
        self.assertIn("--dragonfly-ref 'v1'", str(raised.exception))

    def test_unknown_ref_has_contextual_error(self) -> None:
        with redirect_stdout(io.StringIO()):
            with self.assertRaises(RuntimeError) as raised:
                compat_sync.ensure_checkout(
                    "fixture", str(self.source), self.checkout, "does-not-exist",
                    refresh=False,
                )

        message = str(raised.exception)
        self.assertIn("fixture ref 'does-not-exist'", message)
        self.assertIn(str(self.checkout), message)
        self.assertIn(": ", message)

    def test_main_reports_checkout_failure_without_traceback(self) -> None:
        stderr = io.StringIO()
        with (
            patch.object(compat_sync, "resolve_redis_source", return_value=self.source),
            patch.object(
                compat_sync,
                "resolve_dragonfly_source",
                side_effect=RuntimeError("missing ref"),
            ),
            patch.object(
                compat_sync.sys,
                "argv",
                ["compat_sync.py", "--redis-ref", "8.6.4", "--dragonfly-ref", "bad"],
            ),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            self.assertEqual(compat_sync.main(), 2)

        self.assertEqual(
            stderr.getvalue().strip(),
            "ERROR: source checkout failed: missing ref",
        )


class ReviewFailureTests(unittest.TestCase):
    def test_main_writes_deterministic_artifacts_before_review_failure_exit(self) -> None:
        row = compat_sync.CompatRow("String", "GET", "supported")
        assessment = compat_sync.Assessment(row, "supported", "")
        review_error = {
            "type": "review-error",
            "command": "GET",
            "family": "String",
            "status": "supported",
            "message": "temporary API failure",
        }
        review_flag = {
            "type": "review-flag",
            "command": "SET",
            "family": "String",
            "status": "supported",
            "suggested_status": "partial",
            "message": "A concrete option may be missing.",
        }

        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            generated = root / "generated"
            args = SimpleNamespace(
                add_missing_rows=False,
                filter=[],
                input=root / "compatibility.md",
                limit=0,
                output=root / "compatibility.md",
                progress_every=0,
                review=True,
                review_model="gpt-5.6-terra",
                review_workers=1,
                write_table=True,
            )
            parser = SimpleNamespace(parse_args=lambda: args)

            def write_artifacts(out_dir, *_args, extra_tasks=None, **_kwargs):
                out_dir.mkdir(parents=True)
                (out_dir / "tasks.json").write_text(
                    json.dumps({"tasks": extra_tasks or []}), encoding="utf-8",
                )

            stderr = io.StringIO()
            with (
                patch.dict(os.environ, {"OPENAI_API_KEY": "test"}, clear=True),
                patch.multiple(
                    compat_sync,
                    add_cli_args=lambda: parser,
                    create_client=lambda: SimpleNamespace(close=lambda: None),
                    REPO_ROOT=root,
                    COMPAT_GENERATED=generated,
                    resolve_redis_source=lambda _args: root,
                    resolve_dragonfly_source=lambda _args: root,
                    parse_compat_table=lambda _path: ("before\n", [row], "after\n"),
                    load_redis_specs_from_checkout=lambda _root: {},
                    resolve_module_sources=lambda _args: {"search": root},
                    load_module_specs=lambda _dirs: {
                        "GET": compat_sync.RedisCommandSpec("GET"),
                    },
                    module_source_versions=lambda _dirs: {"search": "test@sha"},
                    DragonflySource=lambda _root: SimpleNamespace(registered={"GET"}),
                    missing_command_tasks=lambda *_args: [],
                    build_assessments=lambda *_args: [assessment],
                    review_assessments=lambda *_args: ([review_flag], [review_error]),
                    write_artifacts=write_artifacts,
                    verification_note=lambda _args: "verified",
                    render_compat_table=lambda *_args: "rendered\n",
                ),
                redirect_stdout(io.StringIO()),
                redirect_stderr(stderr),
            ):
                result = compat_sync.main()

            self.assertEqual(result, 2)
            artifact_dirs = list(generated.iterdir())
            self.assertEqual(len(artifact_dirs), 1)
            payload = json.loads((artifact_dirs[0] / "tasks.json").read_text())
            self.assertEqual(payload["tasks"], [review_flag, review_error])
            self.assertEqual(args.output.read_text(), "rendered\n")
            self.assertIn("deterministic outputs were written", stderr.getvalue())


class CuratedDetailsTests(unittest.TestCase):
    def apply(self, curated: tuple[str, str], derived: tuple[str, str]):
        row = compat_sync.CompatRow("Server", "MEMORY USAGE", curated[0], curated[1])
        assessment = compat_sync.Assessment(row, derived[0], derived[1],
                                            deterministic_change=True)
        [out], change_log = compat_sync.assessments_to_rows([row], [assessment])
        return out, change_log

    def test_prose_in_a_missing_list_is_not_an_option_token(self) -> None:
        row = compat_sync.CompatRow("Server", "MEMORY USAGE", "partial",
                                    "Missing: SAMPLES, which is accepted but ignored.")
        self.assertEqual(compat_sync._curated_missing_tokens(row), {"SAMPLES"})
        self.assertEqual(compat_sync._missing_tokens("Missing: MALLOC-STATS, ignored."),
                         {"MALLOC-STATS"})

    def test_note_on_an_unchanged_unsupported_row_is_kept_and_rendered(self) -> None:
        out, change_log = self.apply(("unsupported", "Use MEMORY DECOMMIT instead."),
                                     ("unsupported", ""))
        self.assertEqual(out.details, "Use MEMORY DECOMMIT instead.")
        self.assertEqual(change_log, [])
        self.assertIn("Use MEMORY DECOMMIT instead.",
                      compat_sync.render_compat_table("", [out], ""))

    def test_curated_wording_is_kept_while_the_missing_options_are_the_same(self) -> None:
        curated = "Missing: SAMPLES, which is accepted but ignored."
        out, change_log = self.apply(("partial", curated), ("partial", "Missing: SAMPLES."))
        self.assertEqual(out.details, curated)
        self.assertEqual(change_log, [])

    def test_tokens_with_digits_are_options(self) -> None:
        self.assertEqual(compat_sync._missing_tokens("Missing: ANDOR, DIFF1, ONE."),
                         {"ANDOR", "DIFF1", "ONE"})

    def test_missing_list_on_a_non_partial_row_is_not_kept(self) -> None:
        out, [entry] = self.apply(("supported", "Missing: BIT."), ("supported", ""))
        self.assertEqual(out.details, "")
        self.assertEqual(entry["replaced_details"], "Missing: BIT.")

    def test_wording_that_names_another_option_is_not_kept(self) -> None:
        row = compat_sync.CompatRow("Connection", "CLIENT KILL", "partial",
                                    "Missing: MAXAGE, SKIPME, USER, laddr.")
        a = compat_sync.Assessment(row, "partial", "Missing: MAXAGE, SKIPME, USER.",
                                   deterministic_change=True,
                                   option_tokens=["LADDR", "MAXAGE", "SKIPME", "USER"])
        [out], [entry] = compat_sync.assessments_to_rows([row], [a])
        self.assertEqual(out.details, "Missing: MAXAGE, SKIPME, USER.")
        self.assertEqual(entry["replaced_details"], "Missing: MAXAGE, SKIPME, USER, laddr.")

    def test_escaped_pipe_round_trips(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            page = Path(temporary_dir) / "compatibility.md"
            page.write_text(
                "| Command Family | Command | Dragonfly Support | Details |\n"
                "|:--|:--|:--|:--|\n"
                '| <span class="family">Server</span> | <span class="command">MEMORY PURGE</span> '
                '| <span class="support unsupported">Unsupported</span> | Use A \\| B instead. |\n'
            )
            before, rows, after = compat_sync.parse_compat_table(page)
            self.assertEqual(rows[0].details, "Use A | B instead.")
            first = compat_sync.render_compat_table(before, rows, after)
            page.write_text(first)
            before, rows, after = compat_sync.parse_compat_table(page)
            self.assertEqual(rows[0].details, "Use A | B instead.")
            self.assertEqual(compat_sync.render_compat_table(before, rows, after), first)

    def test_curated_text_is_replaced_and_logged_when_the_verdict_changes(self) -> None:
        curated = "Missing: SAMPLES, which is accepted but ignored."
        for derived in (("partial", "Missing: SAMPLES, TOP."), ("supported", "")):
            out, [entry] = self.apply(("partial", curated), derived)
            self.assertEqual(out.details, derived[1])
            self.assertEqual(entry["replaced_details"], curated)


class DirtyWriteTableTests(unittest.TestCase):
    def test_write_table_is_refused_for_a_dirty_labelled_checkout(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            dfly = root / "dfly"
            (dfly / "src").mkdir(parents=True)
            for args in (["init", "--quiet"], ["config", "user.name", "T"],
                         ["config", "user.email", "t@example.com"]):
                subprocess.run(["git", *args], cwd=dfly, check=True, capture_output=True)
            (dfly / "src" / "a.cc").write_text("one")
            subprocess.run(["git", "add", "."], cwd=dfly, check=True, capture_output=True)
            subprocess.run(["git", "commit", "--quiet", "-m", "one"], cwd=dfly, check=True,
                           capture_output=True)
            (dfly / "src" / "a.cc").write_text("edited")
            page = root / "compatibility.md"
            page.write_text("original\n")
            args = SimpleNamespace(
                add_missing_rows=False, filter=[], limit=0, input=page, output=page,
                progress_every=0, review=False, write_table=True, dragonfly_ref="v2.0.0",
            )
            stderr = io.StringIO()
            with (
                patch.multiple(
                    compat_sync,
                    add_cli_args=lambda: SimpleNamespace(parse_args=lambda: args),
                    resolve_redis_source=lambda _args: root,
                    resolve_dragonfly_source=lambda _args: dfly,
                    parse_compat_table=lambda _path: ("", [], ""),
                    load_redis_specs_from_checkout=lambda _root: {},
                    resolve_module_sources=lambda _args: {},
                    load_module_specs=lambda _dirs: {"GET": compat_sync.RedisCommandSpec("GET")},
                    module_source_versions=lambda _dirs: {},
                    DragonflySource=lambda _root: self.fail("must stop before indexing"),
                ),
                redirect_stdout(io.StringIO()),
                redirect_stderr(stderr),
            ):
                self.assertEqual(compat_sync.main(), 2)
            self.assertEqual(page.read_text(), "original\n")
            self.assertIn("--write-table refused", stderr.getvalue())


class DragonflySourceTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.root = Path(temporary_dir.name)
        self.server = self.root / "src" / "server"
        self.server.mkdir(parents=True)

    def write_source(self, name: str, source: str) -> None:
        (self.server / name).write_text(textwrap.dedent(source), encoding="utf-8")

    def test_follows_callbacks_templates_and_unique_shared_helpers(self) -> None:
        self.write_source(
            "family_utils.h",
            """
            template <class P = long> consteval auto ExpiryOneOf() {
              return OneOf("", TagValue<P>("EX", nullptr));
            }

            template <class P = long> consteval auto ExpiryOrPersist() {
              return OneOf("", ExpiryOneOf<P>(), Exist("PERSIST", nullptr));
            }
            """,
        )
        self.write_source(
            "example_family.cc",
            """
            Args ParseExpireArgs(Parser* parser) {
              return parser->Options("NX", "XX");
            }

            void CmdExpire(Parser parser) {
              parser.Next(ParseExpireArgs);
            }

            template <Output output>
            void ExpireTimeGeneric(Parser parser) {
              parser.ExpectTag("FIELDS");
            }

            void CmdExpireTime(Parser parser) {
              ExpireTimeGeneric<Output::Milliseconds>(parser);
            }

            void CmdGetEx(Parser parser) {
              auto options = ExpiryOrPersist<Value>();
            }

            void Register(Registry* registry) {
              *registry << CI{"EXPIRE", 0}.HFUNC(Expire)
                        << CI{"HPEXPIRETIME", 0}.HFUNC(ExpireTime)
                        << CI{"GETEX", 0}.HFUNC(GetEx);
            }
            """,
        )

        source = compat_sync.DragonflySource(self.root)

        expire = source.implementation("EXPIRE")
        self.assertTrue(compat_sync._token_honored("NX", expire))
        self.assertTrue(compat_sync._token_honored("XX", expire))
        self.assertTrue(
            compat_sync._token_honored("FIELDS", source.implementation("HPEXPIRETIME")),
        )
        getex = source.implementation("GETEX")
        self.assertTrue(compat_sync._token_honored("EX", getex))
        self.assertTrue(compat_sync._token_honored("PERSIST", getex))

    def test_includes_only_the_referenced_file_scope_grammar(self) -> None:
        self.write_source(
            "example_family.cc",
            """
            constexpr auto kUsedGrammar =
                Compile(Options(Exist("USED", nullptr)));
            constexpr auto kUnusedGrammar =
                Compile(Options(Exist("UNRELATED", nullptr)));

            void CmdCompiled(Parser parser) {
              kUsedGrammar.Apply(&parser);
            }

            void Register(Registry* registry) {
              *registry << CI{"COMPILED", 0}.HFUNC(Compiled);
            }
            """,
        )

        implementation = compat_sync.DragonflySource(self.root).implementation("COMPILED")

        self.assertTrue(compat_sync._token_honored("USED", implementation))
        self.assertFalse(compat_sync._token_honored("UNRELATED", implementation))

    def test_default_braces_do_not_absorb_a_sibling_function(self) -> None:
        source = """
            void ParseCount(Parser* parser, string_view error = {}) {
              parser->Check("ANY");
            }

            void ParseSibling(Parser* parser) {
              parser->Check("UNRELATED");
            }
        """
        text = textwrap.dedent(source)

        span = compat_sync._find_definition_in_text(text, "ParseCount")

        self.assertIsNotNone(span)
        assert span is not None
        body = text[span[0]:span[1]]
        self.assertIn('"ANY"', body)
        self.assertNotIn('"UNRELATED"', body)

    def test_trailing_return_function_does_not_absorb_a_sibling(self) -> None:
        text = textwrap.dedent(
            """
            auto First(Parser* parser) -> Result {
              return Parse(parser);
            }

            void Sibling(Parser* parser) {
              parser->Check("UNRELATED");
            }
            """,
        )

        span = compat_sync._find_definition_in_text(text, "First")

        self.assertIsNotNone(span)
        assert span is not None
        body = text[span[0]:span[1]]
        self.assertIn("return Parse(parser);", body)
        self.assertNotIn('"UNRELATED"', body)
        self.assertEqual(
            [match.group("name") for match in compat_sync._FN_DEF_RE.finditer(text)],
            ["First", "Sibling"],
        )

    def test_mapnext_does_not_walk_sibling_subcommand_callbacks(self) -> None:
        body = (
            'parser.MapNext("CREATE", &CreateGroup, '
            '"SETID", &SetId);'
        )

        self.assertEqual(compat_sync._delegate_callees(body, set()), [])

    def test_follows_family_manager_run_for_parent_subcommands(self) -> None:
        self.write_source(
            "memory_cmd.cc",
            """
            void MemoryCmd::Run(Parser parser) {
              string subcommand = parser.Next();
              if (subcommand == "STATS") {
                SendStats();
              }
            }
            """,
        )
        self.write_source(
            "server_family.cc",
            """
            void ServerFamily::Memory(Parser parser) {
              MemoryCmd memory_cmd;
              memory_cmd.Run(parser);
            }

            void Register(Registry* registry) {
              *registry << CI{"MEMORY", 0}.HFUNC(Memory);
            }
            """,
        )

        source = compat_sync.DragonflySource(self.root)

        self.assertTrue(source.command_exists("MEMORY STATS"))
        self.assertFalse(source.command_exists("MEMORY UNKNOWN"))

    def test_curated_tokens_missing_from_upstream_spec_are_rechecked(self) -> None:
        self.write_source(
            "bloom_family.cc",
            """
            void CmdInfo(Parser parser) {
              parser.Check("CAPACITY");
            }

            void Register(Registry* registry) {
              *registry << CI{"BF.INFO", 0}.HFUNC(Info);
            }
            """,
        )
        row = compat_sync.CompatRow(
            family="Bloom Filter",
            command="BF.INFO",
            status="partial",
            details="Missing: ERROR, TIGHTENING.",
        )
        spec = compat_sync.RedisCommandSpec(
            name="BF.INFO",
            group="bf",
            tokens=["CAPACITY"],
        )

        assessment = compat_sync.deterministic_assessment(
            row,
            spec,
            compat_sync.DragonflySource(self.root),
        )

        self.assertEqual(assessment.proposed_status, "partial")
        self.assertEqual(
            assessment.unsupported_details,
            "Missing: ERROR, TIGHTENING.",
        )
        self.assertIn("upstream-spec-gap", {task["type"] for task in assessment.tasks})

    def test_public_module_source_supplement_fills_commands_json_gap(self) -> None:
        module = self.root / "module"
        (module / "src").mkdir(parents=True)
        (module / "commands.json").write_text("{}", encoding="utf-8")
        (module / "src" / "rebloom.c").write_text(
            'RegisterCommand(ctx, "cf.compact", Handler, "readonly", "read");',
            encoding="utf-8",
        )

        specs = compat_sync.load_module_specs({"bloom": module})

        self.assertIn("CF.COMPACT", specs)
        self.assertEqual(specs["CF.COMPACT"].group, "cf")


if __name__ == "__main__":
    unittest.main()
