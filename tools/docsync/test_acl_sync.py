from __future__ import annotations

import io
import json
import tempfile
import textwrap
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.docsync import acl_sync

COMMAND_ACL = {
    "CLIENT": ["@CONNECTION", "@SLOW"],
    "ACL": ["@CONNECTION"],
    "ACL SETUSER": ["@ADMIN", "@DANGEROUS", "@SLOW"],
    "GET": ["@FAST", "@READ", "@STRING"],
    "XGROUP": ["@SLOW"],
    "_XGROUP_HELP": ["@READ", "@SLOW", "@STREAM"],
}


def page(title: str, body: str) -> str:
    return f"# {title}\n\n## Syntax\n\n    {title}\n\n{textwrap.dedent(body)}"


class AclSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.root = Path(temporary_dir.name)
        self.docs = self.root / "docs" / "command-reference"
        self.docs.mkdir(parents=True)
        patcher = patch.multiple(acl_sync, REPO_ROOT=self.root, DOCS_DIR=self.docs)
        patcher.start()
        self.addCleanup(patcher.stop)

    def write(self, rel: str, text: str) -> Path:
        path = self.docs / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path

    def process(self, path: Path, commands: frozenset[str] = frozenset()) -> acl_sync.PageResult:
        return acl_sync.process_page(path, COMMAND_ACL, dry_run=False, server_commands=commands)

    def test_server_categories_prefer_own_entry_then_parent(self) -> None:
        self.assertEqual(acl_sync.server_categories("ACL SETUSER", COMMAND_ACL),
                         (["@admin", "@dangerous", "@slow"], None))
        self.assertEqual(acl_sync.server_categories("CLIENT LIST", COMMAND_ACL),
                         (["@connection", "@slow"], "CLIENT"))
        self.assertEqual(acl_sync.server_categories("XINFO STREAM", COMMAND_ACL), (None, None))
        self.assertEqual(acl_sync.server_categories("XGROUP CREATE", COMMAND_ACL),
                         (["@slow"], "XGROUP"))
        self.assertEqual(acl_sync.server_categories("XGROUP HELP", COMMAND_ACL),
                         (["@read", "@slow", "@stream"], None))

    def test_subcommand_page_is_synced_to_parent_categories(self) -> None:
        path = self.write("client-list.md", page(
            "CLIENT LIST", "**ACL categories:** @admin, @slow, @dangerous, @connection\n"))
        result = self.process(path)
        self.assertEqual(result.status, "updated")
        self.assertEqual(result.inherited_from, "CLIENT")
        self.assertIn("**ACL categories:** @slow, @connection\n", path.read_text())

    def test_container_page_without_acl_line_is_a_failure(self) -> None:
        # Container pages on the site carry the command's ACL line (CONFIG, MEMORY, ...).
        container = self.write("client.md", page(
            "CLIENT", "This is a container command for client connection commands.\n"))
        result = self.process(container)
        self.assertEqual(result.status, "failed")
        self.assertEqual(result.expected, ["@connection", "@slow"])

    def test_container_page_with_acl_line_is_still_synced(self) -> None:
        path = self.write("client.md", page(
            "CLIENT", "**ACL categories:** @slow\n\nThis is a container command for clients.\n"))
        self.assertEqual(self.process(path).status, "updated")

    def test_server_command_without_acl_category_is_reported_not_touched(self) -> None:
        text = page("RANDOMKEY", "**ACL categories:** @keyspace, @read, @slow\n")
        path = self.write("randomkey.md", text)
        result = self.process(path, frozenset({"RANDOMKEY"}))
        self.assertEqual(result.status, "overview")
        self.assertIn("no ACL category", result.reason)
        self.assertEqual(path.read_text(), text)

    def test_unpublished_pages_are_not_discovered(self) -> None:
        self.write("pubsub/_unsupported/xgroup.md", page("XGROUP", "text\n"))
        self.write("_draft.md", page("GET", "text\n"))
        kept = self.write("strings/get.md", page("GET", "text\n"))
        self.assertEqual(acl_sync.discover_pages(""), [kept])

    def test_dry_run_skips_the_llm_repair_pass(self) -> None:
        self.write("get.md", page("GET", "Returns the value.\n"))
        facts = self.root / "facts.json"
        facts.write_text(json.dumps({"data": {"command_acl": COMMAND_ACL, "commands": {}}}))
        with (
            patch.object(acl_sync, "llm_repair_failed", side_effect=AssertionError("no LLM")),
            patch.object(acl_sync.sys, "argv", ["acl_sync.py", "--facts", str(facts), "--dry-run"]),
            patch.dict(acl_sync.os.environ, {"OPENAI_API_KEY": "test"}),
            redirect_stdout(io.StringIO()) as out,
        ):
            self.assertEqual(acl_sync.main(), 1)
        self.assertIn("LLM repair skipped: --dry-run", out.getvalue())
        self.assertIn("expected: **ACL categories:** @fast, @read, @string", out.getvalue())


if __name__ == "__main__":
    unittest.main()
