#!/usr/bin/env python3
"""acl_sync.py — Synchronize ACL category lines in command-reference docs.

Captures ACL ground truth from a Dragonfly Docker image (via dfly_facts.py)
and updates every command-reference page whose H1 matches a server command.

Updates are minimal-diff:
  * If the *set* of categories on a page already equals the server set, the
    file is not touched at all.
  * If they differ, categories that stay in both keep their original order;
    new categories are appended (alphabetically); categories the server no
    longer reports are dropped.

At the end the script prints an explicit list of pages that could not be
patched (no ACL line where one is required, ambiguous match, etc.) so a
human can decide what to do next.

Usage:
    python tools/docsync/acl_sync.py --tag v1.38.0
    python tools/docsync/acl_sync.py --tag v1.38.0 --dry-run
    python tools/docsync/acl_sync.py --facts tools/generated/facts/v1.38.0.json
    python tools/docsync/acl_sync.py --tag v1.38.0 --filter "search/*"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from fnmatch import fnmatch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs" / "command-reference"
FACTS_DIR = REPO_ROOT / "tools" / "generated" / "facts"
DFLY_FACTS = REPO_ROOT / "tools" / "docsync" / "dfly_facts.py"

H1_RE = re.compile(r"^#[ \t]+(?P<name>[^\n]+?)\s*$", re.MULTILINE)
ACL_LINE_RE = re.compile(
    r"^(?P<prefix>[ \t]*[\-*]?[ \t]*\*\*ACL[ \t]+categor(?:y|ies):\*\*)"
    r"[ \t]*(?P<tail>[^\n]*?)[ \t]*$",
    re.MULTILINE | re.IGNORECASE,
)
CATEGORY_RE = re.compile(r"@[A-Za-z][A-Za-z0-9_-]*")


@dataclass
class PageResult:
    path: Path
    command: str | None = None
    status: str = ""           # updated | unchanged | overview | failed
    reason: str = ""
    old: list[str] = field(default_factory=list)
    new: list[str] = field(default_factory=list)
    via: str = "mechanical"    # "mechanical" | "llm"


# --- Facts loading -----------------------------------------------------------

def load_facts(args: argparse.Namespace) -> dict:
    if args.facts:
        return json.loads(args.facts.read_text(encoding="utf-8"))
    facts_path = FACTS_DIR / f"{args.tag}.json"
    if facts_path.exists() and not args.refresh_facts:
        print(f"  using cached facts: {facts_path.relative_to(REPO_ROOT)}")
        return json.loads(facts_path.read_text(encoding="utf-8"))
    cmd = ["python3", str(DFLY_FACTS), "--tag", args.tag]
    if args.skip_pull:
        cmd.append("--skip-pull")
    print("  capturing facts via dfly_facts.py...")
    p = subprocess.run(cmd)
    if p.returncode != 0 or not facts_path.exists():
        raise RuntimeError("dfly_facts capture failed")
    return json.loads(facts_path.read_text(encoding="utf-8"))


# --- Page parsing ------------------------------------------------------------

def extract_command(text: str) -> str | None:
    """Return the canonical uppercase command name for a page, or None."""
    m = H1_RE.search(text)
    if not m:
        return None
    name = m.group("name").strip().strip("`").strip()
    name = re.sub(r"\s+", " ", name)
    return name.upper() or None


def parse_acl_line(text: str) -> tuple[re.Match | None, list[str], int]:
    """Return (first_match, ordered_categories, total_match_count)."""
    matches = list(ACL_LINE_RE.finditer(text))
    if not matches:
        return None, [], 0
    m = matches[0]
    raw = CATEGORY_RE.findall(m.group("tail"))
    seen: set[str] = set()
    ordered: list[str] = []
    for c in raw:
        cl = c.lower()
        if cl not in seen:
            ordered.append(cl)
            seen.add(cl)
    return m, ordered, len(matches)


# --- Diff logic --------------------------------------------------------------

def reconcile(doc: list[str], server: list[str]) -> tuple[list[str] | None, list[str], list[str]]:
    """Compute the new category list, preserving existing order for kept items.

    Returns (new_list_or_None, added, removed). `None` means the sets are
    equal and the file should not be touched.
    """
    server_set = {c.lower() for c in server}
    doc_set = set(doc)
    if doc_set == server_set:
        return None, [], []
    kept = [c for c in doc if c in server_set]
    added = sorted(c for c in server_set if c not in doc_set)
    removed = [c for c in doc if c not in server_set]
    return kept + added, added, removed


def render(prefix: str, cats: list[str]) -> str:
    return f"{prefix} {', '.join(cats)}"


# --- LLM repair for FAILED pages --------------------------------------------

LLM_REPAIR_MODEL = "claude-sonnet-4-6"
LLM_REPAIR_MAX_TOKENS = 8000

LLM_REPAIR_SYSTEM = """\
You repair the ACL category metadata on a Dragonfly DB documentation page.

You will receive the current page text, the command name, the list of ACL
categories the live server reports for this command, and the reason the
deterministic patcher could not handle the page (e.g. "no ACL line",
"multiple ACL lines").

Decide ONE action and output JSON only.

  1. action = "skip" — when the page is *intentionally* without an ACL
     line. This applies when the page is a container / navigation page:
     its body is mostly a list of subcommand pages, with language like
     "This is a container command for ...", "To see the list of available
     commands you can call XYZ HELP", or just a bulleted list of links to
     sibling pages. Such pages do not have a single ACL set — each
     subcommand has its own page.

  2. action = "patch" — when the page documents the command and should
     have an ACL line. Insert exactly ONE line of the form

         **ACL categories:** @cat1, @cat2, ...

     Use a leading `- ` if and only if the surrounding metadata block on
     the page already uses bullets (e.g. there is a `- **Time complexity:** ...`
     line nearby). Otherwise use the plain form without a leading dash.

     Placement rules, in priority order:
       (a) If the page contains a `**Time complexity:**` line, put the new
           line directly after it (with the same indentation / leading-dash
           style as that line).
       (b) Else, place the new line just after the H1 and the first
           Syntax block (whether fenced ``` or 4-space indented), with one
           blank line on each side.

     Use exactly the categories given to you in the prompt. Sort them
     alphabetically. Do NOT change anything else on the page — no
     description rewrites, no whitespace tweaks elsewhere, no front-matter
     edits. The diff between input and output must be additive only:
     exactly one new line (and at most one blank line of padding around
     it).

     If the page already has multiple ACL lines, keep only the first
     (closest to the metadata block) and remove the duplicates, replacing
     the surviving line's category list with the server-provided
     categories in alphabetical order.

Output strictly this JSON, with no fences and no commentary:

  { "action": "skip" | "patch",
    "reason": "<one sentence explaining the decision>",
    "patched_markdown": "<full file content if action=patch, else empty>" }
"""


def _build_repair_user_text(
    page_text: str, command: str, server_cats: list[str], failure_reason: str,
) -> str:
    return (
        f"=== command ===\n{command}\n\n"
        f"=== expected ACL categories (alphabetical) ===\n"
        f"{', '.join(sorted(server_cats))}\n\n"
        f"=== detector finding ===\n{failure_reason}\n\n"
        f"=== current page ===\n{page_text}\n\n"
        f"=== task ===\n"
        f"Decide skip/patch and produce the JSON. JSON only.\n"
    )


def _call_repair_llm(client, system_prompt: str, user_text: str) -> dict:
    response = client.messages.create(
        model=LLM_REPAIR_MODEL,
        max_tokens=LLM_REPAIR_MAX_TOKENS,
        system=[{"type": "text", "text": system_prompt,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_text}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    return json.loads(text)


def _validate_llm_patch(patched: str, expected_cats: set[str]) -> str | None:
    """Return None on pass, error string on failure."""
    m, parsed_cats, count = parse_acl_line(patched)
    if count != 1:
        return f"patch produced {count} ACL line(s), expected exactly 1"
    got = set(parsed_cats)
    if got != expected_cats:
        missing = expected_cats - got
        extra = got - expected_cats
        bits = []
        if missing:
            bits.append(f"missing {sorted(missing)}")
        if extra:
            bits.append(f"extra {sorted(extra)}")
        return f"patch had wrong categories: {'; '.join(bits)}"
    return None


def llm_repair_failed(
    results: list[PageResult],
    command_acl: dict[str, list[str]],
    dry_run: bool,
) -> None:
    """In-place: try to repair every result with status='failed' via LLM.

    On success the result is mutated to status='updated' or 'overview'
    with via='llm'. On failure the original 'failed' status is kept and
    the LLM's complaint is appended to `reason`.
    """
    failed = [r for r in results if r.status == "failed"]
    if not failed:
        return
    if not os.getenv("ANTHROPIC_API_KEY"):
        for r in failed:
            r.reason += " (LLM repair skipped: ANTHROPIC_API_KEY not set)"
        return
    try:
        import anthropic
    except ImportError:
        for r in failed:
            r.reason += " (LLM repair skipped: anthropic SDK not installed)"
        return

    print(f"\nLLM repair pass over {len(failed)} failed page(s)...")
    client = anthropic.Anthropic()
    for r in failed:
        if not r.command or r.command not in command_acl:
            continue
        server_cats = sorted(c.lower() for c in command_acl[r.command])
        page_text = r.path.read_text(encoding="utf-8")
        user_text = _build_repair_user_text(
            page_text, r.command, server_cats, r.reason,
        )
        try:
            resp = _call_repair_llm(client, LLM_REPAIR_SYSTEM, user_text)
        except Exception as e:
            r.reason += f" (LLM call failed: {e})"
            continue
        action = (resp.get("action") or "").lower()
        llm_reason = (resp.get("reason") or "").strip()
        if action == "skip":
            r.status = "overview"
            r.reason = f"LLM marked as container/overview: {llm_reason}"
            r.via = "llm"
            print(f"  ⊘ {r.path.relative_to(REPO_ROOT)}: skip — {llm_reason}")
            continue
        if action != "patch":
            r.reason += f" (LLM returned unknown action {action!r})"
            print(f"  ✗ {r.path.relative_to(REPO_ROOT)}: bad action {action!r}")
            continue
        patched = resp.get("patched_markdown") or ""
        if not patched.strip():
            r.reason += " (LLM said 'patch' but returned empty markdown)"
            print(f"  ✗ {r.path.relative_to(REPO_ROOT)}: empty patch")
            continue
        err = _validate_llm_patch(patched, set(server_cats))
        if err:
            r.reason += f" (LLM patch rejected: {err})"
            print(f"  ✗ {r.path.relative_to(REPO_ROOT)}: {err}")
            continue
        # Validation passed — apply.
        r.old = []
        r.new = server_cats
        r.status = "updated"
        r.via = "llm"
        r.reason = f"LLM-inserted ACL line: {llm_reason}"
        if not dry_run:
            r.path.write_text(patched, encoding="utf-8")
        print(f"  ✓ {r.path.relative_to(REPO_ROOT)}: patched with "
              f"{', '.join(server_cats)}")


# --- Main --------------------------------------------------------------------

def discover_pages(filter_glob: str) -> list[Path]:
    pages = sorted(DOCS_DIR.rglob("*.md"))
    if filter_glob:
        pages = [p for p in pages
                 if fnmatch(str(p.relative_to(DOCS_DIR)), filter_glob)]
    return pages


def process_page(path: Path, command_acl: dict, dry_run: bool) -> PageResult:
    text = path.read_text(encoding="utf-8")
    res = PageResult(path=path)
    cmd = extract_command(text)
    res.command = cmd
    if not cmd:
        res.status = "overview"
        res.reason = "no H1 — not a command page"
        return res
    if cmd not in command_acl:
        res.status = "overview"
        res.reason = f"H1 {cmd!r} is not a server command"
        return res
    server_cats = sorted(c.lower() for c in command_acl[cmd])
    m, doc_cats, count = parse_acl_line(text)
    if not m:
        res.status = "failed"
        res.reason = "page documents a real command but has no `**ACL categor(y|ies):**` line"
        return res
    if count > 1:
        res.status = "failed"
        res.reason = f"{count} ACL lines found — manual review needed"
        return res
    new_list, added, removed = reconcile(doc_cats, server_cats)
    res.old = doc_cats
    if new_list is None:
        res.status = "unchanged"
        res.new = doc_cats
        return res
    res.new = new_list
    if not dry_run:
        new_text = text[:m.start()] + render(m.group("prefix"), new_list) + text[m.end():]
        path.write_text(new_text, encoding="utf-8")
    res.status = "updated"
    bits: list[str] = []
    if added:
        bits.append(f"+{','.join(added)}")
    if removed:
        bits.append(f"-{','.join(removed)}")
    res.reason = " ".join(bits)
    return res


def report(results: list[PageResult], dry_run: bool) -> int:
    counters = {"updated": 0, "unchanged": 0, "overview": 0, "failed": 0}
    via_counts = {"mechanical": 0, "llm": 0}
    overview_via_llm = 0
    for r in results:
        counters[r.status] += 1
        if r.status == "updated":
            via_counts[r.via] += 1
        if r.status == "overview" and r.via == "llm":
            overview_via_llm += 1

    print("")
    print(f"Pages walked:  {len(results)}")
    print(f"  updated:     {counters['updated']}  "
          f"(mechanical {via_counts['mechanical']}, llm {via_counts['llm']})")
    print(f"  unchanged:   {counters['unchanged']}")
    print(f"  not a cmd:   {counters['overview']}  "
          f"(silently skipped — {overview_via_llm} of them recognized as "
          f"container/overview by the LLM repair pass)")
    print(f"  failed:      {counters['failed']}")

    if counters["updated"]:
        suffix = " (dry-run — no files written)" if dry_run else ""
        print(f"\n=== Updated {counters['updated']} page(s){suffix} ===")
        for r in results:
            if r.status != "updated":
                continue
            rel = r.path.relative_to(REPO_ROOT)
            tag = " [LLM]" if r.via == "llm" else ""
            print(f"  {rel}  ({r.command}){tag}")
            print(f"      old: {', '.join(r.old) or '(none)'}")
            print(f"      new: {', '.join(r.new)}")
            if r.reason:
                print(f"      change: {r.reason}")

    if overview_via_llm:
        print(f"\n=== {overview_via_llm} page(s) classified as container/overview "
              f"by the LLM repair pass ===")
        for r in results:
            if r.status == "overview" and r.via == "llm":
                rel = r.path.relative_to(REPO_ROOT)
                print(f"  {rel}  ({r.command})")
                print(f"      {r.reason}")

    if counters["failed"]:
        print(f"\n=== UPDATE FAILED on {counters['failed']} page(s) — manual review needed ===")
        for r in results:
            if r.status != "failed":
                continue
            rel = r.path.relative_to(REPO_ROOT)
            print(f"  {rel}")
            print(f"    command: {r.command}")
            print(f"    reason:  {r.reason}")
        return 1
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tag", help="Dragonfly tag (e.g. v1.38.0).")
    g.add_argument("--facts", type=Path,
                   help="Path to a pre-captured facts JSON.")
    ap.add_argument("--skip-pull", action="store_true",
                    help="Skip docker pull when capturing facts.")
    ap.add_argument("--refresh-facts", action="store_true",
                    help="Re-capture facts even if a cached file exists.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Show planned changes without writing.")
    ap.add_argument("--filter", default="",
                    help="Glob (relative to docs/command-reference/) "
                         "to limit which pages are processed.")
    ap.add_argument("--no-llm", action="store_true",
                    help="Skip the LLM repair pass for pages without an "
                         "ACL line.")
    args = ap.parse_args()

    facts = load_facts(args)
    command_acl = facts["data"]["command_acl"]
    print(f"  ground truth: {len(command_acl)} commands with ACL data")

    pages = discover_pages(args.filter)
    print(f"  scanning {len(pages)} page(s) under docs/command-reference/")

    results = [process_page(p, command_acl, args.dry_run) for p in pages]

    if not args.no_llm and any(r.status == "failed" for r in results):
        llm_repair_failed(results, command_acl, args.dry_run)

    return report(results, args.dry_run)


if __name__ == "__main__":
    sys.exit(main())
