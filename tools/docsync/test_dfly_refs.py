from __future__ import annotations

import io
import json
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from tools.docsync import dfly_facts, dfly_refs, docs_sync, flags_sync

SHA_A = "a" * 40
SHA_B = "b" * 40


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=cwd, capture_output=True, text=True, check=True,
    ).stdout.strip()


class GitFixture(unittest.TestCase):
    """An upstream repo plus a cached clone of it, like /tmp/dragonfly-docsync."""

    def setUp(self) -> None:
        temporary_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temporary_dir.cleanup)
        self.root = Path(temporary_dir.name)
        self.upstream = self.root / "upstream"
        self.checkout = self.root / "checkout"
        self.upstream.mkdir()
        git(self.upstream, "init", "--quiet")
        git(self.upstream, "config", "user.name", "Docsync Test")
        git(self.upstream, "config", "user.email", "docsync@example.com")
        self.commit("one", "v1")

    def commit(self, content: str, tag: str | None = None) -> str:
        (self.upstream / "content.txt").write_text(content, encoding="utf-8")
        git(self.upstream, "add", "content.txt")
        git(self.upstream, "commit", "--quiet", "-m", content)
        if tag:
            git(self.upstream, "tag", "--force", tag)
        return git(self.upstream, "rev-parse", "HEAD")

    def ensure(self, tag: str) -> str:
        with redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
            return dfly_refs.ensure_checkout(self.checkout, tag, str(self.upstream))


class EnsureCheckoutTests(GitFixture):
    def test_tag_that_moved_upstream_is_refetched(self) -> None:
        self.ensure("v1")
        moved = self.commit("moved", "v1")

        self.assertEqual(self.ensure("v1"), moved)
        self.assertEqual(git(self.checkout, "rev-parse", "HEAD"), moved)

    def test_tag_created_after_clone_is_fetched(self) -> None:
        self.ensure("v1")
        two = self.commit("two", "v2")

        self.assertEqual(self.ensure("v2"), two)

    def test_unknown_tag_raises_instead_of_keeping_the_old_tree(self) -> None:
        self.ensure("v1")
        with self.assertRaises(RuntimeError) as raised:
            self.ensure("v9")
        self.assertIn("'v9' does not exist", str(raised.exception))

    def test_current_tag_is_not_refetched(self) -> None:
        self.ensure("v1")
        with patch.object(dfly_refs, "fetch_tags", side_effect=AssertionError("no fetch")):
            self.assertEqual(self.ensure("v1"), git(self.upstream, "rev-parse", "v1"))

    def test_unreachable_upstream_uses_local_tag_with_one_warning(self) -> None:
        self.ensure("v1")
        missing = str(self.root / "gone.git")
        stderr = io.StringIO()
        with (
            patch.object(dfly_refs, "fetch_tags", side_effect=AssertionError("no fetch")),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            commit = dfly_refs.ensure_checkout(self.checkout, "v1", missing)
            with patch.object(dfly_refs, "run", side_effect=AssertionError("host is memoized")):
                self.assertEqual(dfly_refs.upstream_tag_lookup("v1", missing), (False, None))
        self.assertEqual(commit, git(self.upstream, "rev-parse", "v1"))
        self.assertEqual(stderr.getvalue().count("WARNING"), 1)

    def test_tag_deleted_upstream_is_an_error_even_if_fetch_fails(self) -> None:
        self.ensure("v1")
        git(self.upstream, "tag", "-d", "v1")
        failed = subprocess.CompletedProcess([], 1, "", "fetch failed")
        with patch.object(dfly_refs, "fetch_tags", return_value=failed):
            with self.assertRaises(RuntimeError) as raised:
                self.ensure("v1")
        self.assertIn("does not exist upstream", str(raised.exception))

    def test_dirty_checkout_is_rejected(self) -> None:
        self.ensure("v1")
        (self.checkout / "untracked.cc").write_text("// local edit")
        with self.assertRaises(RuntimeError) as raised:
            self.ensure("v1")
        self.assertIn("local changes", str(raised.exception))

    def test_branch_name_is_rejected(self) -> None:
        with self.assertRaises(RuntimeError):
            self.ensure(git(self.upstream, "branch", "--show-current"))

    def test_tag_deleted_upstream_is_not_used(self) -> None:
        self.ensure("v1")
        self.commit("two", "v2")
        git(self.upstream, "tag", "-d", "v1")
        with self.assertRaises(RuntimeError):
            self.ensure("v1")

    def test_upstream_tag_lookup_distinguishes_missing_tag_and_unreachable_remote(self) -> None:
        stderr = io.StringIO()
        with redirect_stderr(stderr):
            self.assertEqual(
                dfly_refs.upstream_tag_lookup("v1", str(self.upstream)),
                (True, git(self.upstream, "rev-parse", "v1")),
            )
            self.assertEqual(dfly_refs.upstream_tag_lookup("v9", str(self.upstream)), (True, None))
            self.assertEqual(stderr.getvalue(), "")
            self.assertEqual(
                dfly_refs.upstream_tag_lookup("v1", str(self.root / "missing.git")),
                (False, None),
            )
        self.assertIn("could not query", stderr.getvalue())


class RunTests(unittest.TestCase):
    def test_missing_binary_and_timeout_are_failed_processes(self) -> None:
        missing = dfly_refs.run(["docsync-no-such-binary"])
        self.assertEqual(missing.returncode, 127)
        self.assertIn("cannot run", missing.stderr)
        slow = dfly_refs.run([sys.executable, "-c", "import time; time.sleep(5)"], timeout=0.2)
        self.assertEqual(slow.returncode, 124)


class FactsStalenessTests(unittest.TestCase):
    def facts(self, commit: str | None) -> dict:
        return {"meta": {"dragonfly_commit": commit} if commit else {}}

    def staleness(self, facts: dict, upstream: str | None, image: str | None,
                  reachable: bool | None = None) -> str | None:
        """upstream=None means GitHub was unreachable unless reachable=True."""
        def image_version(_ref):
            if image is None:
                raise RuntimeError("not available locally")
            return f"dragonfly v2.0.0-{image}", image

        lookup = (upstream is not None if reachable is None else reachable, upstream)
        with (
            patch.object(dfly_refs, "upstream_tag_lookup", return_value=lookup),
            patch.object(dfly_refs, "image_version", side_effect=image_version),
            redirect_stderr(io.StringIO()),
        ):
            return dfly_refs.facts_staleness(facts, "v2.0.0", "img:v2.0.0")

    def test_matching_commits_are_current(self) -> None:
        self.assertIsNone(self.staleness(self.facts(SHA_A), SHA_A, SHA_A))
        self.assertIsNone(self.staleness(self.facts(SHA_A), None, None))

    def test_moved_tag_makes_facts_stale(self) -> None:
        self.assertIn("moved upstream", self.staleness(self.facts(SHA_A), SHA_B, SHA_A))

    def test_rebuilt_image_makes_facts_stale(self) -> None:
        self.assertIn("local image", self.staleness(self.facts(SHA_A), None, SHA_B))

    def test_tag_missing_upstream_makes_facts_stale(self) -> None:
        self.assertIn("does not exist upstream",
                      self.staleness(self.facts(SHA_A), None, SHA_A, reachable=True))

    def test_facts_without_commit_are_stale(self) -> None:
        self.assertIn("no meta.dragonfly_commit",
                      self.staleness(self.facts(None), SHA_A, SHA_A))

    def test_load_facts_recaptures_stale_cache(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            facts_dir = Path(temporary_dir)
            (facts_dir / "v2.0.0.json").write_text(json.dumps(self.facts(SHA_A)))
            calls = []

            def fake_capture(cmd):
                calls.append(cmd)
                (facts_dir / "v2.0.0.json").write_text(json.dumps(self.facts(SHA_B)))
                return SimpleNamespace(returncode=0)

            with (
                patch.object(dfly_refs, "facts_staleness", return_value="tag moved"),
                patch.object(dfly_refs.subprocess, "run", side_effect=fake_capture),
                redirect_stdout(io.StringIO()),
            ):
                facts = dfly_refs.load_facts("v2.0.0", facts_dir, "img:v2.0.0",
                                             skip_pull=True, refresh=False)

        self.assertEqual(dfly_refs.facts_commit(facts), SHA_B)
        self.assertIn("--skip-pull", calls[0])
        self.assertIn(str(facts_dir / "v2.0.0.json"), calls[0])

    def test_check_same_commit_ignores_unknown_and_rejects_mismatch(self) -> None:
        dfly_refs.check_same_commit("v2.0.0", source=SHA_A, image=SHA_A, facts=None)
        with self.assertRaises(RuntimeError) as raised:
            dfly_refs.check_same_commit("v2.0.0", source=SHA_A, image=SHA_B)
        self.assertIn("different commits", str(raised.exception))


class DfFactsCaptureTests(unittest.TestCase):
    def capture(self, *, upstream: str | None, helpfull: str,
                version: tuple[str, str | None] = (f"dragonfly v2.0.0-{SHA_A}", SHA_A),
                ) -> tuple[int, str]:
        stderr = io.StringIO()
        with (
            patch.object(dfly_facts.sys, "argv", ["dfly_facts.py", "--tag", "v2.0.0",
                                                   "--skip-pull", "--output", "/nonexistent"]),
            patch.object(dfly_facts, "image_version", return_value=version),
            patch.object(dfly_facts, "upstream_tag_lookup", return_value=(True, upstream)),
            patch.object(dfly_facts, "docker_image_digest", return_value="sha256:x"),
            patch.object(dfly_facts, "docker_image_labels", return_value=("sha256:x", {})),
            patch.object(dfly_facts, "docker_helpfull", return_value=helpfull),
            patch.object(dfly_facts, "docker_run_dragonfly",
                         side_effect=AssertionError("must not boot")),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            return dfly_facts.main(), stderr.getvalue()

    def test_image_from_another_commit_than_the_tag_is_rejected(self) -> None:
        code, err = self.capture(upstream=SHA_B, helpfull="")
        self.assertEqual(code, 1)
        self.assertIn("Rebuild or re-pull", err)

    def test_empty_helpfull_is_rejected(self) -> None:
        code, err = self.capture(upstream=SHA_A, helpfull="")
        self.assertEqual(code, 1)
        self.assertIn("no flags", err)

    def test_tag_missing_upstream_is_rejected(self) -> None:
        code, err = self.capture(upstream=None, helpfull="")
        self.assertEqual(code, 1)
        self.assertIn("refusing to capture", err)
        self.assertNotIn("no flags", err)

    def test_image_without_build_sha_is_rejected(self) -> None:
        code, err = self.capture(upstream=SHA_A, helpfull="",
                                 version=("dragonfly dev-0000000", None))
        self.assertEqual(code, 1)
        self.assertIn("no build commit SHA", err)


class DocsSyncDiscoverTests(GitFixture):
    def test_prompt_lists_every_changed_file_with_src_first(self) -> None:
        for i in range(250):
            path = self.upstream / "fuzz" / f"seed{i:03}"
            path.parent.mkdir(exist_ok=True)
            path.write_text(str(i))
        server = self.upstream / "src" / "server" / "string_family.cc"
        server.parent.mkdir(parents=True)
        server.write_text("// changed")
        git(self.upstream, "add", ".")
        git(self.upstream, "commit", "--quiet", "-m", "big change")
        git(self.upstream, "tag", "v2")

        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream)),
            redirect_stdout(io.StringIO()),
        ):
            diff = docs_sync.collect_source_diff_summary("v1", "v2")
            prompt = docs_sync.build_discover_prompt(diff, [])

        self.assertEqual(len(diff["files"]), 251)
        files_section = prompt.split("files_changed (251;", 1)[1]
        self.assertTrue(files_section.split("\n", 2)[1].startswith("src/server/string_family.cc"))
        self.assertIn("fuzz/seed249 +1 -0", prompt)
        self.assertNotIn("omitted", prompt)

    def test_rename_is_listed_as_real_paths(self) -> None:
        git(self.upstream, "mv", "content.txt", "renamed.txt")
        git(self.upstream, "commit", "--quiet", "-m", "rename")
        git(self.upstream, "tag", "v2")
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream)),
            redirect_stdout(io.StringIO()),
        ):
            diff = docs_sync.collect_source_diff_summary("v1", "v2")
        self.assertEqual(sorted(diff["files_changed"]), ["content.txt", "renamed.txt"])

    def test_empty_range_only_plans_also_update_pages(self) -> None:
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream), PLANS_DIR=self.root / "plans",
                           REPO_ROOT=self.root, DOCS_DIR=self.root / "docs",
                           create_client=lambda: self.fail("LLM must not be called")),
            patch.dict(docs_sync.os.environ, {"OPENAI_API_KEY": "test"}),
            redirect_stdout(io.StringIO()),
            redirect_stderr(io.StringIO()),
        ):
            plan = docs_sync.discover_phase("v1", "v1", ["docs/a.md"], "")
            with self.assertRaises(RuntimeError):
                docs_sync.discover_phase("v1", "v1", [], "")
        self.assertEqual([e["path"] for e in plan["files_to_update"]], ["docs/a.md"])
        self.assertEqual(plan["after_commit"], git(self.upstream, "rev-parse", "v1"))

    def test_dry_run_discover_neither_calls_openai_nor_saves_a_plan(self) -> None:
        self.commit("two", "v2")
        plans = self.root / "plans"
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream), PLANS_DIR=plans,
                           REPO_ROOT=self.root, DOCS_DIR=self.root / "docs",
                           create_client=lambda: self.fail("LLM must not be called")),
            patch.dict(docs_sync.os.environ, {"OPENAI_API_KEY": "test"}),
            redirect_stdout(io.StringIO()),
        ):
            plan = docs_sync.discover_phase("v1", "v2", [], "", dry_run=True)
        self.assertEqual(plan["files_to_update"], [])
        self.assertFalse(plans.exists())

    def test_moved_before_tag_is_not_resolved_to_the_stale_commit(self) -> None:
        self.ensure("v1")
        self.commit("two", "v2")
        self.commit("moved", "v1")
        failed = subprocess.CompletedProcess([], 1, "", "fetch failed")
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream)),
            patch.object(dfly_refs, "fetch_tags", return_value=failed),
            redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()),
            self.assertRaises(RuntimeError),
        ):
            docs_sync.resolve_before("v1")

    def test_before_accepts_a_revision_that_is_not_a_tag(self) -> None:
        sha = git(self.upstream, "rev-parse", "v1")
        self.commit("two", "v2")
        self.ensure("v2")
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream)),
            redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()),
        ):
            self.assertEqual(docs_sync.resolve_before(sha), sha)
            self.assertEqual(docs_sync.resolve_before("v2~1"), sha)

    def test_before_tag_deleted_upstream_raises(self) -> None:
        self.ensure("v1")
        git(self.upstream, "tag", "-d", "v1")
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream)),
            redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()),
            self.assertRaises(RuntimeError) as raised,
        ):
            docs_sync.resolve_before("v1")
        self.assertIn("does not exist upstream", str(raised.exception))

    def test_discover_plans_only_normalized_unowned_docs_paths(self) -> None:
        root = self.root / "repo"
        (root / "docs" / "managing-dragonfly").mkdir(parents=True)
        (root / "docs" / "managing-dragonfly" / "flags.md").write_text("# Flags\n")
        (root / "docs" / "get.md").write_text("# GET\n")
        diff = {"before": "v1", "after": "v2", "commits": ["abc x"], "files": [],
                "files_changed": [], "before_commit": "a", "after_commit": "b"}
        llm_paths = ["docs/x/../managing-dragonfly/flags.md", "README.md", "./docs/get.md"]

        class Client:
            def close(self): pass

        with (
            patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs",
                           PLANS_DIR=root / "plans",
                           collect_source_diff_summary=lambda *_a: diff,
                           build_diff_context=lambda *_a: None,
                           create_client=Client,
                           call_llm_streaming=lambda *_a: (
                               {"files_to_update": [{"path": p, "reason": "r"} for p in llm_paths]},
                               {"input_tokens": 0, "output_tokens": 0, "reasoning_tokens": 0})),
            patch.dict(docs_sync.os.environ, {"OPENAI_API_KEY": "test"}),
            redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()),
        ):
            plan = docs_sync.discover_phase(
                "v1", "v2", ["docs/managing-dragonfly/flags.md", "../x.md", "docs/get.md"], "")
        self.assertEqual([e["path"] for e in plan["files_to_update"]], ["docs/get.md"])
        self.assertEqual(plan["manual_overrides"], ["docs/get.md"])

    def test_missing_before_tag_raises(self) -> None:
        self.commit("two", "v2")
        with (
            patch.multiple(docs_sync, DRAGONFLY_CHECKOUT=self.checkout,
                           DRAGONFLY_REPO_URL=str(self.upstream)),
            redirect_stdout(io.StringIO()),
            self.assertRaises(RuntimeError),
        ):
            docs_sync.collect_source_diff_summary("v0", "v2")


class DocsSyncDockerBootTests(unittest.TestCase):
    def test_page_is_not_updated_when_docker_does_not_boot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            page = root / "docs" / "get.md"
            page.parent.mkdir()
            original = "# GET\n\n```shell\ndragonfly> GET k\n(nil)\n```\n"
            page.write_text(original)
            facts = {"data": {"commands": {"GET": {"arity": 2}}, "command_acl": {}}}

            with (
                patch.multiple(
                    docs_sync,
                    REPO_ROOT=root,
                    DOCS_DIR=root / "docs",
                    boot_docker=lambda *_a, **_k: (_ for _ in ()).throw(RuntimeError("No such image")),
                    create_client=lambda: self.fail("LLM must not be called"),
                    find_command_handler_source=lambda *_a: None,
                ),
                patch.dict(docs_sync.os.environ, {"OPENAI_API_KEY": "test"}),
            ):
                result = docs_sync.update_one_file(
                    {"path": "docs/get.md"}, "v2.0.0", facts, root, dry_run=False,
                )

            self.assertEqual(result["status"], "failed")
            self.assertIn("No such image", result["error"])
            self.assertEqual(page.read_text(), original)


class DocsSyncUpdatePreflightTests(unittest.TestCase):
    def setUp(self) -> None:
        image = patch.object(docs_sync.dfly_refs, "image_version",
                             return_value=(f"dragonfly v2.0.0-{SHA_A}", SHA_A))
        image.start()
        self.addCleanup(image.stop)

    def update(self, plan: dict) -> str:
        stderr = io.StringIO()
        with (
            patch.object(docs_sync, "ensure_dragonfly_checkout", return_value=SHA_A),
            patch.multiple(docs_sync.dfly_refs,
                           docker_pull=lambda _ref: None,
                           load_facts=lambda *_a, **_k: {"meta": {"dragonfly_commit": SHA_A}}),
            redirect_stdout(io.StringIO()),
            redirect_stderr(stderr),
        ):
            docs_sync.update_phase(plan, "v2.0.0", skip_pull=True, dry_run=True)
        return stderr.getvalue()

    def test_plan_discovered_before_the_tag_moved_is_refused(self) -> None:
        with self.assertRaises(RuntimeError) as raised:
            self.update({"after_commit": SHA_B, "files_to_update": []})
        self.assertIn("re-run discover", str(raised.exception))

    def test_plan_whose_before_tag_moved_is_refused(self) -> None:
        with (
            patch.object(docs_sync, "resolve_before", return_value=SHA_B),
            self.assertRaises(RuntimeError) as raised,
        ):
            self.update({"before": "v1.40.0", "before_commit": SHA_A,
                         "after_commit": SHA_A, "files_to_update": []})
        self.assertIn("v1.40.0 is now", str(raised.exception))

    def test_image_without_build_sha_is_refused(self) -> None:
        with (
            patch.object(docs_sync.dfly_refs, "image_version",
                         return_value=("dragonfly dev-0000000", None)),
            self.assertRaises(RuntimeError) as raised,
        ):
            self.update({"after_commit": SHA_A, "files_to_update": []})
        self.assertIn("no build commit SHA", str(raised.exception))

    def test_update_phase_normalizes_paths_before_filtering(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            (root / "docs" / "strings").mkdir(parents=True)
            (root / "docs" / "strings" / "get.md").write_text("# GET\n")
            plan = {"after_commit": SHA_A, "files_to_update": [
                {"path": "./docs/strings/get.md"}, {"path": None}]}
            with patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs"):
                with patch.object(docs_sync, "ensure_dragonfly_checkout", return_value=SHA_A), \
                        patch.multiple(docs_sync.dfly_refs, docker_pull=lambda _ref: None,
                                       load_facts=lambda *_a, **_k: {"meta": {"dragonfly_commit": SHA_A}}), \
                        redirect_stdout(io.StringIO()):
                    results = docs_sync.update_phase(plan, "v2.0.0", skip_pull=True, dry_run=True,
                                                     filter_glob="strings/*")
        self.assertEqual([(r["path"], r["status"]) for r in results],
                         [("docs/strings/get.md", "skipped"), (None, "failed")])

    def test_plan_without_commits_warns(self) -> None:
        self.assertIn("no after_commit", self.update({"files_to_update": []}))
        self.assertEqual(self.update({"after_commit": SHA_A, "files_to_update": []}), "")

    def test_boot_failure_reports_docker_stderr(self) -> None:
        error = subprocess.CalledProcessError(125, ["docker", "run"], stderr="Conflict. name in use")
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            (root / "docs").mkdir()
            (root / "docs" / "get.md").write_text("# GET\n")
            facts = {"data": {"commands": {"GET": {"arity": 2}}, "command_acl": {}}}
            with patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs",
                                boot_docker=lambda *_a, **_k: (_ for _ in ()).throw(error),
                                find_command_handler_source=lambda *_a: None):
                result = docs_sync.update_one_file(
                    {"path": "docs/get.md"}, "v2.0.0", facts, root, dry_run=False,
                )
        self.assertIn("Conflict. name in use", result["error"])

    def test_owned_or_outside_paths_never_reach_the_plan_or_a_write(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            (root / "docs" / "managing-dragonfly").mkdir(parents=True)
            (root / "docs" / "managing-dragonfly" / "flags.md").write_text("# Flags\n")
            (root / "docs" / "get.md").write_text("# GET\n")
            with patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs",
                                boot_docker=lambda *_a, **_k: self.fail("must not boot"),
                                create_client=lambda: self.fail("must not call OpenAI")), \
                    redirect_stdout(io.StringIO()), redirect_stderr(io.StringIO()):
                sneaky = docs_sync.update_one_file(
                    {"path": "docs/managing-dragonfly/../managing-dragonfly/flags.md"},
                    "v2.0.0", {}, root, dry_run=False)
                outside = docs_sync.update_one_file(
                    {"path": "docs/../README.md"}, "v2.0.0", {}, root, dry_run=False)
                planned = [docs_sync.plannable_path(p, "--also-update") for p in
                           ("docs/managing-dragonfly/flags.md", "./docs/get.md", "/etc/passwd")]
        self.assertEqual((sneaky["status"], sneaky["path"]),
                         ("skipped", "docs/managing-dragonfly/flags.md"))
        self.assertEqual(outside["status"], "failed")
        self.assertEqual(planned, [None, "docs/get.md", None])

    def test_pages_owned_by_other_scripts_are_never_edited(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            flags = root / "docs" / "managing-dragonfly" / "flags.md"
            flags.parent.mkdir(parents=True)
            flags.write_text("# Flags\n")
            (root / "docs" / "get.md").write_text("# GET\n")
            with patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs",
                                boot_docker=lambda *_a, **_k: self.fail("must not boot"),
                                create_client=lambda: self.fail("must not call OpenAI")):
                index = [e["path"] for e in docs_sync.collect_md_index()]
                result = docs_sync.update_one_file(
                    {"path": "docs/managing-dragonfly/flags.md"}, "v2.0.0", {}, root,
                    dry_run=False,
                )
        self.assertEqual(index, ["docs/get.md"])
        self.assertEqual(result["status"], "skipped")
        self.assertIn("flags_sync.py", result["error"])

    def test_filter_accepts_repo_and_docs_relative_globs(self) -> None:
        for glob in ("docs/command-reference/strings/*", "command-reference/strings/*", ""):
            self.assertTrue(docs_sync.matches_filter("docs/command-reference/strings/get.md", glob))
        self.assertFalse(docs_sync.matches_filter("docs/command-reference/strings/get.md",
                                                  "command-reference/lists/*"))

    def test_dry_run_does_not_boot_or_call_openai(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            root = Path(temporary_dir)
            (root / "docs").mkdir()
            (root / "docs" / "get.md").write_text("# GET\n")
            facts = {"data": {"commands": {"GET": {"arity": 2}}, "command_acl": {}}}
            with patch.multiple(docs_sync, REPO_ROOT=root, DOCS_DIR=root / "docs",
                                boot_docker=lambda *_a, **_k: self.fail("must not boot"),
                                create_client=lambda: self.fail("must not call OpenAI")):
                result = docs_sync.update_one_file(
                    {"path": "docs/get.md"}, "v2.0.0", facts, root, dry_run=True,
                )
        self.assertEqual(result["status"], "skipped")


class FlagsSyncSourceCacheTests(unittest.TestCase):
    def run_capture(self, source_dir: Path, cache_commit: str | None, facts_commit: str,
                    parser: int = flags_sync.SOURCE_PARSER_VERSION) -> tuple[dict, list[str]]:
        cache = source_dir / "v2.0.0.json"
        if cache_commit:
            cache.write_text(json.dumps({"tag": "v2.0.0", "commit": cache_commit, "parser": parser,
                                         "flags": {"port": {"cached": True}}}))
        checkouts: list[str] = []

        def ensure_checkout(_checkout, tag, _repo):
            checkouts.append(tag)
            return facts_commit

        args = SimpleNamespace(tag="v2.0.0", refresh_source=False)
        with (
            patch.multiple(flags_sync, SOURCE_DIR=source_dir, REPO_ROOT=source_dir,
                           extract_source_facts=lambda *_a, **_k: {"port": {"parsed": True}}),
            patch.object(flags_sync.dfly_refs, "ensure_checkout", side_effect=ensure_checkout),
            redirect_stdout(io.StringIO()),
        ):
            facts = flags_sync.load_or_capture_source(args, {"port"}, facts_commit)
        return facts, checkouts

    def test_cache_from_the_same_commit_is_reused(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            facts, checkouts = self.run_capture(Path(temporary_dir), SHA_A, SHA_A)
        self.assertEqual(facts, {"port": {"cached": True}})
        self.assertEqual(checkouts, [])

    def test_cache_from_an_older_parser_is_reparsed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            facts, checkouts = self.run_capture(Path(temporary_dir), SHA_A, SHA_A, parser=1)
        self.assertEqual(facts, {"port": {"parsed": True}})
        self.assertEqual(checkouts, ["v2.0.0"])

    def test_cache_from_another_commit_is_reparsed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_dir:
            source_dir = Path(temporary_dir)
            facts, checkouts = self.run_capture(source_dir, SHA_B, SHA_A)
            written = json.loads((source_dir / "v2.0.0.json").read_text())
        self.assertEqual(facts, {"port": {"parsed": True}})
        self.assertEqual(checkouts, ["v2.0.0"])
        self.assertEqual(written["commit"], SHA_A)


if __name__ == "__main__":
    unittest.main()
