from __future__ import annotations

import io
import json
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

from tools.docsync import flags_sync


def absl_flag(name: str, default: str, help_text: str) -> str:
    return f'ABSL_FLAG(bool, {name}, {default}, "{help_text}");\n'


class SourceParserTests(unittest.TestCase):
    def test_escapes_are_decoded(self) -> None:
        self.assertEqual(
            flags_sync._join_string_literals(r'"a:\n - b,\t\"c\"" "\\d \x41\101\0"'),
            'a:\n - b,\t"c"\\d AA\0',
        )

    def test_digit_separator_is_not_a_char_literal(self) -> None:
        text = ('ABSL_FLAG(uint32_t, budget, 50\'000, "Budget in ns");\n'
                'ABSL_FLAG(uint32_t, mask, 0xFFFF\'FFFF, "Mask");\n'
                'ABSL_FLAG(char8_t, digit, u8\'0\', "Digit");\n'
                "void F() { char c = ')'; }\n")
        decls = [(d["name"], d["default_expr"], d["description"])
                 for d in flags_sync.parse_absl_flags(text)]
        self.assertEqual(decls, [("budget", "50'000", "Budget in ns"),
                                 ("mask", "0xFFFF'FFFF", "Mask"),
                                 ("digit", "u8'0'", "Digit")])

    def test_server_declaration_wins_over_test_and_bench_redeclarations(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            src = Path(temporary_dir)
            files = {
                "src/server/dfly_bench.cc": absl_flag("tcp_nodelay", "false", "bench"),
                "src/facade/dragonfly_connection.cc": absl_flag("tcp_nodelay", "true", "server"),
                "src/server/test_utils.cc": absl_flag("force_epoll", "false", "tests"),
                "src/server/dfly_main.cc": absl_flag("force_epoll", "false", "server")
                + "int main(int argc, char* argv[]) {}\n",
                "src/facade/ok_main.cc": absl_flag("port", "0", "no-op in ok_backend")
                + "int main(int argc, char* argv[]) {}\n",
                "src/server/main_service.cc": absl_flag("port", "6379", "server"),
            }
            for rel, text in files.items():
                (src / rel).parent.mkdir(parents=True, exist_ok=True)
                (src / rel).write_text(text)
            names = {"tcp_nodelay", "force_epoll", "port"}
            with redirect_stdout(io.StringIO()):
                grouped = flags_sync.extract_source_facts(src, names, groups={
                    "tcp_nodelay": "facade/dragonfly_connection.cc",
                    "force_epoll": "server/dfly_main.cc",
                })
                ungrouped = flags_sync.extract_source_facts(src, names)
        for facts in (grouped, ungrouped):
            self.assertEqual(facts["tcp_nodelay"]["description"], "server")
            self.assertEqual(facts["tcp_nodelay"]["default_expr"], "true")
            self.assertEqual(facts["force_epoll"]["description"], "server")
            self.assertEqual(facts["port"]["description"], "server")


class DryRunTests(unittest.TestCase):
    def test_dry_run_neither_calls_openai_nor_writes_the_page(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            flags_page = root / "flags.md"
            text = "### `--port`\n\n`default: 1`\n\nRedis port.\n"
            flags_page.write_text(text)
            facts = root / "facts.json"
            facts.write_text(json.dumps({"tag": "v2.0.0", "meta": {}, "data": {"flags": {
                "port": {"default": "6379", "description": "Redis port.", "type": "int32",
                         "group": "server/main_service.cc"},
            }}}))
            with (
                patch.multiple(flags_sync, FLAGS_PAGE=flags_page, SOURCE_DIR=root / "source",
                               create_client=lambda: self.fail("must not call OpenAI"),
                               load_or_capture_source=lambda *_a, **_k: self.fail("no source")),
                patch.object(flags_sync.sys, "argv",
                             ["flags_sync.py", "--facts", str(facts), "--dry-run"]),
                patch.dict(flags_sync.os.environ, {"OPENAI_API_KEY": "test"}),
                redirect_stdout(io.StringIO()) as out,
            ):
                flags_sync.main()
            self.assertEqual(flags_page.read_text(), text)
        self.assertIn("--dry-run", out.getvalue())


if __name__ == "__main__":
    unittest.main()
