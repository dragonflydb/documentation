from __future__ import annotations

import copy
import io
import json
import tempfile
import textwrap
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.docsync import acl_model, acl_sync

# Shaped like tools/generated/facts/v2.1.0.json: ACL CAT spells subcommands with
# their own bit "CMD|SUB", COMMAND lists ACL subcommands with a space and does
# not list ACL-only entries (CLIENT KILL) or hidden commands (DFLYCLUSTER).
COMMAND_ACL = {
    "ACL": ["@slow"],
    "ACL|SETUSER": ["@admin", "@dangerous", "@slow"],
    "ACL|WHOAMI": ["@slow"],
    "CLIENT": ["@connection", "@slow"],
    "CLIENT|KILL": ["@admin", "@connection", "@dangerous", "@slow"],
    "MEMORY": ["@read", "@slow"],
    "MEMORY|DEFRAGMENT-SEGMENTS": ["@admin", "@dangerous", "@slow"],
    "GET": ["@fast", "@read", "@string"],
    "XGROUP": ["@slow", "@stream", "@write"],
    "XINFO": ["@read", "@slow", "@stream"],
    "_XGROUP_HELP": ["@read", "@slow", "@stream"],
    "DFLYCLUSTER": ["@admin", "@dangerous", "@slow"],
}
COMMANDS = ["ACL", "ACL SETUSER", "ACL WHOAMI", "CLIENT", "MEMORY", "GET", "XGROUP", "XINFO"]


def make_facts(command_acl: dict | None = None, commands: list[str] | None = None) -> dict:
    command_acl = copy.deepcopy(COMMAND_ACL if command_acl is None else command_acl)
    categories: dict[str, list[str]] = {}
    for name, cats in command_acl.items():
        for c in cats:
            categories.setdefault(c, []).append(name)
    return {
        "meta": {"dragonfly_commit": "1bfc6b18e0e48a9a98c730c25c6c8e788eaf2d85"},
        "data": {
            "commands": {c: {} for c in (COMMANDS if commands is None else commands)},
            "command_acl": command_acl,
            "acl_categories": {c: sorted(m) for c, m in sorted(categories.items())},
        },
    }


def page(title: str, body: str) -> str:
    return f"# {title}\n\n## Syntax\n\n    {title}\n\n{textwrap.dedent(body)}"


class ModelTests(unittest.TestCase):
    def setUp(self) -> None:
        self.facts = make_facts()
        self.view = acl_model.command_acl_view(self.facts)
        self.commands = acl_model.server_commands(self.facts)

    def resolve(self, command: str) -> acl_model.Resolution:
        return acl_model.resolve(command, self.view, self.commands)

    def test_resolution_follows_the_server(self) -> None:
        cases = {
            "ACL SETUSER": ("own", "ACL SETUSER", ["@admin", "@dangerous", "@slow"]),
            "CLIENT KILL": ("acl-only", "CLIENT KILL", ["@admin", "@connection", "@dangerous", "@slow"]),
            "CLIENT KILL ID": ("acl-only", "CLIENT KILL", ["@admin", "@connection", "@dangerous", "@slow"]),
            "MEMORY DEFRAGMENT-SEGMENTS": ("acl-only", "MEMORY DEFRAGMENT-SEGMENTS",
                                           ["@admin", "@dangerous", "@slow"]),
            "CLIENT GETNAME": ("inherited", "CLIENT", ["@connection", "@slow"]),
            "MEMORY USAGE": ("inherited", "MEMORY", ["@read", "@slow"]),
            "DFLYCLUSTER GETSLOTINFO": ("inherited", "DFLYCLUSTER", ["@admin", "@dangerous", "@slow"]),
            "XGROUP HELP": ("routed", "_XGROUP_HELP", ["@read", "@slow", "@stream"]),
            "XGROUP HELP X": ("inherited", "XGROUP", ["@slow", "@stream", "@write"]),
            "CLIENT": ("own", "CLIENT", ["@connection", "@slow"]),
        }
        for command, (kind, key, cats) in cases.items():
            with self.subTest(command=command):
                r = self.resolve(command)
                self.assertEqual((r.kind, r.key, r.categories), (kind, key, cats))

    def test_acl_subcommands_never_fall_back_to_acl(self) -> None:
        self.assertEqual(self.resolve("ACL NOSUCH").categories, None)
        self.assertEqual(self.resolve("NOSUCH").categories, None)

    def test_view_accepts_both_spellings_and_rejects_collisions(self) -> None:
        old_shape = make_facts({"ACL SETUSER": ["@ADMIN", "@SLOW"]}, ["ACL SETUSER"])
        self.assertEqual(acl_model.command_acl_view(old_shape), {"ACL SETUSER": ["@admin", "@slow"]})
        clash = make_facts({"ACL SETUSER": ["@admin"], "ACL|SETUSER": ["@slow"]}, ["ACL SETUSER"])
        with self.assertRaises(acl_model.FactsError):
            acl_model.command_acl_view(clash)

    def test_invariants_pass_on_the_normalised_view(self) -> None:
        self.assertEqual(acl_model.invariants(self.facts, self.view), [])

    def test_invariants_catch_the_v2_1_0_spelling_change(self) -> None:
        # The regression behind the v2.1.0 incident: reading the raw "CMD|SUB"
        # keys without normalising them must fail loudly, not resolve quietly.
        raw = {k.upper(): sorted(v) for k, v in COMMAND_ACL.items()}
        problems = acl_model.invariants(self.facts, raw)
        self.assertTrue(any("'ACL|SETUSER'" in p for p in problems))
        self.assertTrue(any("ACL SETUSER: listed by COMMAND but in no ACL category" in p for p in problems))

    def test_invariants_catch_unknown_hidden_entries_and_missing_routes(self) -> None:
        acl = dict(COMMAND_ACL, NEWHIDDEN=["@admin"])
        del acl["_XGROUP_HELP"]
        facts = make_facts(acl)
        problems = acl_model.invariants(facts, acl_model.command_acl_view(facts))
        self.assertTrue(any(p.startswith("NEWHIDDEN:") for p in problems))
        self.assertTrue(any("routed target _XGROUP_HELP is missing" in p for p in problems))

    def test_invariants_catch_a_command_without_categories(self) -> None:
        facts = make_facts(commands=COMMANDS + ["RANDOMKEY"])
        problems = acl_model.invariants(facts, acl_model.command_acl_view(facts))
        self.assertIn("RANDOMKEY: listed by COMMAND but in no ACL category", problems)


class PageTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.root = Path(temporary_dir.name)
        self.docs = self.root / "docs" / "command-reference"
        self.docs.mkdir(parents=True)
        patcher = patch.multiple(acl_sync, REPO_ROOT=self.root, DOCS_DIR=self.docs)
        patcher.start()
        self.addCleanup(patcher.stop)
        facts = make_facts()
        self.view = acl_model.command_acl_view(facts)
        self.commands = acl_model.server_commands(facts)

    def write(self, rel: str, text: str) -> Path:
        path = self.docs / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def process(self, path: Path) -> acl_sync.PageResult:
        return acl_sync.process_page(path, self.view, self.commands)

    def test_acl_subcommand_page_keeps_its_own_categories(self) -> None:
        path = self.write("acl/setuser.md", page(
            "ACL SETUSER", "**ACL categories:** @admin, @slow, @dangerous\n"))
        result = self.process(path)
        self.assertEqual((result.status, result.kind), ("unchanged", "own"))

    def test_acl_only_subcommand_gets_its_own_categories(self) -> None:
        path = self.write("client-kill.md", page("CLIENT KILL", "**ACL categories:** @slow, @connection\n"))
        result = self.process(path)
        self.assertEqual(result.status, "updated")
        self.assertEqual(result.tag(), "[acl-only CLIENT KILL]")
        self.assertIn("**ACL categories:** @slow, @connection, @admin, @dangerous\n", result.new_text)
        self.assertNotIn("@admin", path.read_text(), "process_page must not write")

    def test_inherited_subcommand_gets_the_container_categories(self) -> None:
        path = self.write("client-getname.md", page("CLIENT GETNAME", "**ACL categories:** @slow\n"))
        result = self.process(path)
        self.assertEqual((result.status, result.tag()), ("updated", "[inherited from CLIENT]"))
        self.assertIn("**ACL categories:** @slow, @connection\n", result.new_text)

    def test_versioned_label_is_normalised(self) -> None:
        path = self.write("memory-defragment-segments.md", page(
            "MEMORY DEFRAGMENT-SEGMENTS", "**ACL categories (Dragonfly v2.0.2):** @read, @slow\n"))
        result = self.process(path)
        self.assertEqual(result.status, "updated")
        self.assertIn("**ACL categories:** @slow, @admin, @dangerous\n", result.new_text)
        self.assertNotIn("(Dragonfly", result.new_text)

    def test_matching_set_is_not_touched_even_with_an_odd_label(self) -> None:
        path = self.write("memory-defragment-segments.md", page(
            "MEMORY DEFRAGMENT-SEGMENTS", "**ACL categories (note):** @slow, @admin, @dangerous\n"))
        self.assertEqual(self.process(path).status, "unchanged")

    def test_unrecognised_acl_line_fails_without_the_llm(self) -> None:
        path = self.write("get.md", page("GET", "**ACL categories**: @read\n"))
        result = self.process(path)
        self.assertEqual(result.status, "failed")
        self.assertFalse(result.llm_eligible)
        self.assertIn("unrecognised ACL line", result.reason)

    def test_missing_acl_line_is_left_to_the_llm(self) -> None:
        result = self.process(self.write("get.md", page("GET", "Returns the value.\n")))
        self.assertEqual((result.status, result.llm_eligible), ("failed", True))
        self.assertEqual(result.expected, ["@fast", "@read", "@string"])

    def test_unknown_acl_subcommand_is_not_a_server_command(self) -> None:
        result = self.process(self.write("acl/nosuch.md", page("ACL NOSUCH", "**ACL categories:** @slow\n")))
        self.assertEqual(result.status, "not-synced")

    def test_unpublished_pages_are_not_discovered(self) -> None:
        self.write("pubsub/_unsupported/xgroup.md", page("XGROUP", "text\n"))
        self.write("_draft.md", page("GET", "text\n"))
        kept = self.write("strings/get.md", page("GET", "text\n"))
        self.assertEqual(acl_sync.discover_pages(""), [kept])


class LlmValidatorTests(unittest.TestCase):
    ORIGINAL = "# GET\n\n## Syntax\n\n    GET key\n\n**Time complexity:** O(1)\n\nReturns the value.\n"

    def test_accepts_one_inserted_line(self) -> None:
        patched = self.ORIGINAL.replace("O(1)\n", "O(1)\n\n**ACL categories:** @fast, @read, @string\n")
        self.assertIsNone(acl_sync._validate_llm_patch(self.ORIGINAL, patched, {"@fast", "@read", "@string"}))

    def test_rejects_a_prose_edit(self) -> None:
        patched = self.ORIGINAL.replace("O(1)\n", "O(1)\n\n**ACL categories:** @fast, @read, @string\n")
        patched = patched.replace("Returns the value.", "Returns the stored value.")
        self.assertIn("non-ACL line", acl_sync._validate_llm_patch(self.ORIGINAL, patched, {"@fast", "@read", "@string"}))

    def test_rejects_wrong_categories_and_duplicates(self) -> None:
        one = self.ORIGINAL.replace("O(1)\n", "O(1)\n\n**ACL categories:** @fast, @read\n")
        self.assertIn("wrong categories", acl_sync._validate_llm_patch(self.ORIGINAL, one, {"@fast", "@read", "@string"}))
        two = one.replace("Returns", "**ACL categories:** @fast\n\nReturns")
        self.assertIsNotNone(acl_sync._validate_llm_patch(self.ORIGINAL, two, {"@fast", "@read"}))

    def test_accepts_removing_a_duplicate_acl_line(self) -> None:
        original = self.ORIGINAL.replace("O(1)\n", "O(1)\n\n**ACL categories:** @read\n\n**ACL categories:** @fast\n")
        patched = self.ORIGINAL.replace("O(1)\n", "O(1)\n\n**ACL categories:** @fast, @read, @string\n")
        self.assertIsNone(acl_sync._validate_llm_patch(original, patched, {"@fast", "@read", "@string"}))


class LiveCheckTests(unittest.TestCase):
    def result(self, kind: str, key: str | None, expected: list[str]) -> acl_sync.PageResult:
        return acl_sync.PageResult(path=Path("x.md"), command="CLIENT KILL", kind=kind, key=key, expected=expected)

    @staticmethod
    def replies(allowed: set[str], entry: str) -> dict:
        denied = f"This user has no permissions to run the '{entry}' command"
        out = {f"cat:{c}": ("OK" if c in allowed else denied) for c in ("@admin", "@connection", "@slow", "@read")}
        out.update({"all": "OK", "none": denied})
        return out

    def test_classify(self) -> None:
        self.assertEqual(acl_sync.classify_dryrun("OK"), ("allowed", None))
        self.assertEqual(acl_sync.classify_dryrun(
            "This user has no permissions to run the 'CLIENT KILL' command"), ("denied", "CLIENT KILL"))
        self.assertEqual(acl_sync.classify_dryrun(RuntimeError("Command 'X' not found"))[0], "error")
        self.assertEqual(acl_sync.classify_dryrun("wrong number of arguments")[0], "unknown")

    def test_agreement_and_disagreement(self) -> None:
        res = self.result("acl-only", "CLIENT KILL", ["@admin", "@connection", "@slow"])
        self.assertEqual(acl_sync.check_page_live(res, self.replies({"@admin", "@connection", "@slow"}, "CLIENT KILL")), [])
        stale = self.result("inherited", "CLIENT", ["@connection", "@slow"])
        problems = acl_sync.check_page_live(stale, self.replies({"@admin", "@connection", "@slow"}, "CLIENT KILL"))
        self.assertEqual(len(problems), 2)
        self.assertIn("the server checks CLIENT KILL, acl_sync resolves CLIENT", problems)

    def test_a_server_command_resolved_as_none_is_a_disagreement(self) -> None:
        res = self.result("", None, [])
        self.assertTrue(acl_sync.check_page_live(res, self.replies({"@slow"}, "CLIENT KILL")))
        errors = {k: RuntimeError("Command 'X' not found") for k in self.replies(set(), "X")}
        self.assertEqual(acl_sync.check_page_live(res, errors), [])


class CategoriesPageTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.page = Path(temporary_dir.name) / "acl-categories.md"

    def test_block_is_rendered_between_the_markers(self) -> None:
        self.page.write_text(f"# ACL categories\n\nIntro.\n\n{acl_sync.BLOCK_BEGIN}\nold\n{acl_sync.BLOCK_END}\n\nTail.\n")
        out = acl_sync.update_categories_page(make_facts(), self.page)
        self.assertEqual(out.status, "updated")
        self.assertIn("## `@admin`", out.new_text)
        self.assertIn("`CLIENT|KILL`", out.new_text)
        self.assertTrue(out.new_text.startswith("# ACL categories\n\nIntro.\n"))
        self.assertTrue(out.new_text.endswith("\n\nTail.\n"))
        self.page.write_text(out.new_text)
        self.assertEqual(acl_sync.update_categories_page(make_facts(), self.page).status, "unchanged")

    def test_missing_markers_and_descriptions_fail(self) -> None:
        self.page.write_text("# ACL categories\n")
        self.assertEqual(acl_sync.update_categories_page(make_facts(), self.page).status, "failed")
        self.page.write_text(f"{acl_sync.BLOCK_BEGIN}\n{acl_sync.BLOCK_END}\n")
        facts = make_facts(dict(COMMAND_ACL, GET=["@fast", "@newcat"]))
        out = acl_sync.update_categories_page(facts, self.page)
        self.assertEqual(out.status, "failed")
        self.assertIn("@newcat", out.reason)


class MainTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.root = Path(temporary_dir.name)
        self.docs = self.root / "docs" / "command-reference"
        (self.docs / "acl").mkdir(parents=True)
        self.categories = self.root / "docs" / "managing-dragonfly" / "acl-categories.md"
        self.categories.parent.mkdir(parents=True)
        self.categories.write_text(f"# ACL categories\n\n{acl_sync.BLOCK_BEGIN}\n{acl_sync.BLOCK_END}\n")
        patcher = patch.multiple(acl_sync, REPO_ROOT=self.root, DOCS_DIR=self.docs,
                                 CATEGORIES_PAGE=self.categories)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.setuser = self.docs / "acl" / "setuser.md"
        self.setuser.write_text(page("ACL SETUSER", "**ACL categories:** @slow\n"))

    def run_main(self, facts: dict, *extra: str) -> tuple[int, str, str]:
        path = self.root / "facts.json"
        path.write_text(json.dumps(facts))
        with (
            patch.object(acl_sync.sys, "argv", ["acl_sync.py", "--facts", str(path), *extra]),
            patch.object(acl_sync, "llm_repair_failed", side_effect=AssertionError("no LLM")),
            redirect_stdout(io.StringIO()) as out,
            redirect_stderr(io.StringIO()) as err,
        ):
            code = acl_sync.main()
        return code, out.getvalue(), err.getvalue()

    def test_dry_run_reports_without_writing(self) -> None:
        (self.docs / "get.md").write_text(page("GET", "Returns the value.\n"))
        code, out, _ = self.run_main(make_facts(), "--dry-run", "--no-verify-live")
        self.assertEqual(code, acl_sync.EXIT_PAGES)
        self.assertIn("Live check:    not run (--no-verify-live)", out)
        self.assertIn("LLM repair skipped: --dry-run", out)
        self.assertIn("[own]", out)
        self.assertEqual(self.setuser.read_text(), page("ACL SETUSER", "**ACL categories:** @slow\n"))

    def test_run_writes_pages_and_the_categories_page(self) -> None:
        code, out, _ = self.run_main(make_facts(), "--no-verify-live", "--no-llm")
        self.assertEqual(code, acl_sync.EXIT_OK, out)
        self.assertIn("**ACL categories:** @slow, @admin, @dangerous", self.setuser.read_text())
        self.assertIn("## `@admin`", self.categories.read_text())

    def test_facts_shape_violation_writes_nothing(self) -> None:
        facts = make_facts(dict(COMMAND_ACL, NEWHIDDEN=["@admin"]))
        code, _, err = self.run_main(facts, "--no-verify-live", "--no-llm")
        self.assertEqual(code, acl_sync.EXIT_SHAPE)
        self.assertIn("NEWHIDDEN", err)
        self.assertEqual(self.setuser.read_text(), page("ACL SETUSER", "**ACL categories:** @slow\n"))

    def test_live_check_failure_writes_nothing(self) -> None:
        with patch.object(acl_sync, "verify_live", return_value=(1, ["acl/setuser.md: disagreement"])):
            code, _, err = self.run_main(make_facts(), "--no-llm", "--image", "img:v2.1.0")
        self.assertEqual(code, acl_sync.EXIT_LIVE)
        self.assertIn("nothing was written", err)
        self.assertEqual(self.setuser.read_text(), page("ACL SETUSER", "**ACL categories:** @slow\n"))


if __name__ == "__main__":
    unittest.main()
