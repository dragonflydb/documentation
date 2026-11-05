#!/usr/bin/env python3
"""docs_sync.py — Update doc pages based on Dragonfly source changes between tags.

Two phases. The first is a single LLM call that produces a plan. The second
runs one LLM session per file in that plan, with Docker-verified examples
and the source code at the new tag as factual ground truth.

Phase 1 — Discover:
  * Compute the source-tree diff between <before> and <after> in the
    Dragonfly checkout (commit subjects + per-file stat — never the raw
    diff, which is too noisy and too big).
  * Walk every .md under docs/ and build an index of (path, H1, first
    descriptive paragraph).
  * One LLM call returns a plan: which doc files need updates and why,
    plus optional pointers to relevant source files.
  * If --also-update <file> is given, every path in that file is force-
    appended to the plan even if the LLM said "no change".
  * The plan is saved to tools/generated/update_plans/<ts>.json.

Phase 2 — Update each file:
  * For each entry in the plan, read the current page.
  * Identify the topic (H1 → command name when it matches a real server
    command; otherwise generic page).
  * Pull the relevant source excerpts at <after> (handler body, ABSL_FLAG
    declarations, etc.).
  * Boot a Dragonfly Docker container at <after>. Run every eligible ```shell
    block already on the page in one redis-cli session (FLUSHALL first) and
    capture the actual output. Blocks that require replication, native-cluster,
    failover, or remote-node state are preserved because a standalone container
    cannot verify them; blocks with SUBSCRIBE/PSUBSCRIBE/SSUBSCRIBE/MONITOR are
    preserved because they never return.
  * The LLM produces the updated markdown with strict rules: only facts
    that the source or Docker confirms; general-case complexity only;
    never invent options or behaviors.
  * Changed and new example blocks then run on a fresh container, after the
    unchanged blocks that precede them, and their output replaces the LLM's.
    (The first container keeps the ACL users, CONFIG changes and scripts the
    current examples made.)

CLI:
    python docs_sync.py --before v1.37.0 --after v1.38.0
    python docs_sync.py --before v1.37.0 --after v1.38.0 --also-update extra.txt
    python docs_sync.py --before v1.37.0 --after v1.38.0 --discover-only
    python docs_sync.py --update-only-from tools/generated/update_plans/<ts>.json
    python docs_sync.py --before v1.37.0 --after v1.38.0 --dry-run
    python docs_sync.py --before v1.37.0 --after v1.38.0 --filter "docs/command-reference/strings/*"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shlex
import subprocess
import sys
import time
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path

try:
    from .openai_llm import (
        DEFAULT_BALANCED_MODEL,
        call_json,
        configured_model,
        create_client,
        strict_object_schema,
    )
except ImportError:  # Direct execution: python tools/docsync/docs_sync.py
    from openai_llm import (
        DEFAULT_BALANCED_MODEL,
        call_json,
        configured_model,
        create_client,
        strict_object_schema,
    )

try:
    from . import acl_model, dfly_refs
except ImportError:
    import acl_model
    import dfly_refs

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"
GENERATED = REPO_ROOT / "tools" / "generated"
PLANS_DIR = GENERATED / "update_plans"
LLM_DEBUG_DIR = GENERATED / "llm_debug"
FACTS_DIR = GENERATED / "facts"

# Pages another docsync script owns end to end. docs_sync never plans or edits
# them: its LLM output would overwrite values those scripts validated.
OWNED_PAGES = {
    "docs/managing-dragonfly/flags.md": "flags_sync.py",
    "docs/command-reference/compatibility.md": "compat_sync.py",
}

DRAGONFLY_REPO_URL = "https://github.com/dragonflydb/dragonfly.git"
DRAGONFLY_CHECKOUT = Path("/tmp/dragonfly-docsync")
DRAGONFLY_IMAGE = "docker.dragonflydb.io/dragonflydb/dragonfly"

DISCOVER_MODEL = configured_model(DEFAULT_BALANCED_MODEL)
UPDATE_MODEL = configured_model()
DISCOVER_MAX_TOKENS = 24000
# The discover prompt lists every commit subject and changed file. The caps only
# guard against a pathological range; hitting one prints a warning.
DISCOVER_MAX_COMMITS = 1000
DISCOVER_MAX_FILES = 2000
UPDATE_MAX_TOKENS = 48000
PING_TIMEOUT_S = 30


# --- Helpers ----------------------------------------------------------------

def run(cmd: list[str], cwd: Path | None = None, check: bool = True,
        timeout: float | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check,
                          timeout=timeout)


def ensure_dragonfly_checkout(tag: str) -> str:
    """Check out `tag` at its current upstream commit; return the commit."""
    return dfly_refs.ensure_checkout(DRAGONFLY_CHECKOUT, tag, DRAGONFLY_REPO_URL)


def resolve_before(ref: str) -> str:
    """Commit of --before: a tag (matched to upstream), or any local revision
    when `ref` is a tag neither upstream nor in the checkout. Failures to bring
    a real tag up to date are errors, never a silent fallback to a stale tag."""
    lookup = dfly_refs.upstream_tag_lookup(ref, DRAGONFLY_REPO_URL)
    if lookup[1] or dfly_refs.local_tag_commit(DRAGONFLY_CHECKOUT, ref):
        return dfly_refs.ensure_tag(DRAGONFLY_CHECKOUT, ref, DRAGONFLY_REPO_URL, lookup)
    commit = dfly_refs.resolve_commit(DRAGONFLY_CHECKOUT, ref)
    if not commit:
        raise RuntimeError(f"Dragonfly ref {ref!r} is neither a tag nor a revision in "
                           f"{DRAGONFLY_CHECKOUT}")
    return commit


def normalize_doc_path(path: str) -> str:
    """Repo-relative, normalized path of a page under docs/. Raises ValueError for
    a path outside docs/, so `docs/a/../flags.md` cannot bypass OWNED_PAGES."""
    if not isinstance(path, str) or not path:
        raise ValueError(f"{path!r} is not a page under docs/")
    normalized = Path(os.path.normpath(REPO_ROOT / path))
    try:
        normalized.relative_to(DOCS_DIR)
    except ValueError:
        raise ValueError(f"{path!r} is not a page under docs/") from None
    return str(normalized.relative_to(REPO_ROOT))


def plannable_path(path: str, source: str) -> str | None:
    """Normalized path to put in a plan, or None (with a note) for a path that
    is outside docs/ or owned by another docsync script."""
    try:
        rel = normalize_doc_path(path)
    except ValueError as e:
        print(f"  WARNING: {source}: {e}; not planned", file=sys.stderr)
        return None
    if rel in OWNED_PAGES:
        print(f"  {source}: {rel} is owned by {OWNED_PAGES[rel]}; not planned")
        return None
    if not is_published(rel):
        print(f"  {source}: {rel} is not published (a path part starts with `_`); not planned")
        return None
    return rel


def is_published(rel: str) -> bool:
    """Docusaurus excludes `_`-prefixed files and directories by default."""
    return not any(part.startswith("_") for part in Path(rel).relative_to("docs").parts)


# --- Markdown index ----------------------------------------------------------

H1_RE = re.compile(r"^#[ \t]+(?P<text>[^\n]+?)\s*$", re.MULTILINE)
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)


def extract_h1(text: str) -> str | None:
    m = H1_RE.search(text)
    if not m:
        return None
    return m.group("text").strip().strip("`").strip()


def extract_first_paragraph(text: str, max_chars: int = 400) -> str:
    """Return the first descriptive paragraph after H1, stripped of import
    statements and component tags. Truncated to max_chars."""
    body = FRONTMATTER_RE.sub("", text)
    h1m = H1_RE.search(body)
    if h1m:
        body = body[h1m.end():]
    cleaned: list[str] = []
    for line in body.split("\n"):
        s = line.strip()
        if not s:
            if cleaned:
                break
            continue
        if s.startswith(("import ", "<", "##", "###", "```", "**Time complexity:**",
                         "**ACL")):
            continue
        cleaned.append(s)
        if sum(len(x) for x in cleaned) > max_chars:
            break
    para = " ".join(cleaned).strip()
    if len(para) > max_chars:
        para = para[:max_chars].rstrip() + "…"
    return para


def matches_filter(rel: str, filter_glob: str) -> bool:
    """--filter accepts a repo-relative (docs/...) or docs-relative glob."""
    return (not filter_glob or fnmatch(rel, filter_glob)
            or fnmatch(str(Path(rel).relative_to("docs")) if rel.startswith("docs/") else rel,
                       filter_glob))


def collect_md_index(filter_glob: str = "") -> list[dict]:
    out: list[dict] = []
    for f in sorted(DOCS_DIR.rglob("*.md")):
        rel = str(f.relative_to(REPO_ROOT))
        if rel in OWNED_PAGES or not is_published(rel) or not matches_filter(rel, filter_glob):
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        out.append({
            "path": rel,
            "h1": extract_h1(text),
            "summary": extract_first_paragraph(text),
        })
    return out


# --- Source diff summary -----------------------------------------------------

def collect_source_diff_summary(before: str, after: str) -> dict:
    after_commit = ensure_dragonfly_checkout(after)
    before_commit = resolve_before(before)
    print(f"  diff range: {before} @ {dfly_refs.short(before_commit)} .. "
          f"{after} @ {dfly_refs.short(after_commit)}")
    log = run(["git", "log", "--no-merges", "--pretty=%h %s",
               f"{before_commit}..{after_commit}"], cwd=DRAGONFLY_CHECKOUT).stdout
    # --numstat prints full paths (--stat shortens long ones to ".../"), and
    # --no-renames lists a rename as delete + add instead of "{old => new}".
    numstat = run(["git", "diff", "--numstat", "--no-renames",
                   f"{before_commit}..{after_commit}"], cwd=DRAGONFLY_CHECKOUT).stdout
    files = []
    for line in numstat.splitlines():
        added, deleted, path = line.split("\t", 2)
        files.append({"path": path, "added": added, "deleted": deleted})
    return {
        "before": before,
        "after": after,
        "before_commit": before_commit,
        "after_commit": after_commit,
        "commits": [l for l in log.splitlines() if l.strip()],
        "files": files,
        "files_changed": [f["path"] for f in files],
    }


def commits_touching_file(before: str, after: str, src_file: str) -> list[str]:
    """Return commits between before and after that touched src_file."""
    p = run(
        ["git", "log", "--no-merges", "--pretty=%h %s",
         f"{before}..{after}", "--", src_file],
        cwd=DRAGONFLY_CHECKOUT, check=False,
    )
    return [l for l in p.stdout.splitlines() if l.strip()]


def build_diff_context(diff: dict, related_files: list[str], reason: str) -> dict:
    """Compose the per-file diff_context to pass to the update LLM session."""
    commits_per_file = []
    for f in related_files:
        # Resolved commits, not tag names: a tag may move while discover runs.
        commits = commits_touching_file(diff["before_commit"], diff["after_commit"], f)
        if commits:
            commits_per_file.append({"file": f, "commits": commits})
    return {
        "before": diff["before"],
        "after": diff["after"],
        "discovery_reason": reason,
        "commits_per_file": commits_per_file,
    }


# --- LLM helpers -------------------------------------------------------------

def call_llm_streaming(client, system_prompt: str, user_text: str,
                       max_tokens: int, model: str, schema_name: str,
                       schema: dict) -> tuple[dict, dict]:
    return call_json(
        client,
        system_prompt=system_prompt,
        user_text=user_text,
        schema_name=schema_name,
        schema=schema,
        model=model,
        max_output_tokens=max_tokens,
        stream=True,
    )


# --- Phase 1: Discover -------------------------------------------------------

DISCOVER_SYSTEM = """\
You triage which documentation pages need updating after a Dragonfly DB
release. You receive a summary of source-code changes between two tags
(commit subjects + per-file stat) and an index of every Markdown page
under docs/.

Decide, for each page, whether the source changes plausibly require an
update. Be conservative: only flag a page when there is a credible link
between a commit / changed file and the page's topic. Do not invent
links. Pages whose topic is unrelated to the source changes (e.g. a
generic installation guide unaffected by a server change) should not be
flagged.

Return JSON only — no prose, no markdown fences, no preamble:

  {
    "files_to_update": [
      { "path":  "docs/...md",
        "reason": "<one sentence stating which commit / file motivates this>",
        "related_source_files": ["src/server/...cc", ...] },
      ...
    ],
    "no_update_needed_summary": "<one short sentence about the pages that
                                  were not flagged>"
  }

The output JSON's first character must be `{` and the last must be `}`.
"""

DISCOVER_SCHEMA = strict_object_schema({
    "files_to_update": {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "path": {"type": "string"},
                "reason": {"type": "string"},
                "related_source_files": {
                    "type": "array",
                    "items": {"type": "string"},
                },
            },
            "required": ["path", "reason", "related_source_files"],
            "additionalProperties": False,
        },
    },
    "no_update_needed_summary": {"type": "string"},
})


def omitted_note(total: int, kept: int, what: str) -> str:
    if total <= kept:
        return ""
    print(f"  WARNING: discover prompt omits {total - kept} of {total} {what}",
          file=sys.stderr)
    return f"... {total - kept} more {what} omitted"


def build_discover_prompt(diff: dict, md_index: list[dict]) -> str:
    commits = diff["commits"]
    # Server source first, so a capped list never drops it for fuzz seeds/CI files.
    files = sorted(diff["files"], key=lambda f: not f["path"].startswith("src/"))
    parts = [
        f"=== source diff summary {diff['before']}..{diff['after']} ===",
        f"commits ({len(commits)}):",
        "\n".join(commits[:DISCOVER_MAX_COMMITS]),
        omitted_note(len(commits), DISCOVER_MAX_COMMITS, "commits"),
        "",
        f"files_changed ({len(files)}; +added -deleted lines, src/ first):",
        "\n".join(f"{f['path']} +{f['added']} -{f['deleted']}"
                  for f in files[:DISCOVER_MAX_FILES]),
        omitted_note(len(files), DISCOVER_MAX_FILES, "files"),
        "",
        f"=== docs index ({len(md_index)} markdown files) ===",
        json.dumps(md_index, indent=2, ensure_ascii=False),
        "",
        "=== task ===",
        "Produce the JSON {files_to_update, no_update_needed_summary}.",
        "JSON only.",
    ]
    return "\n".join(p for p in parts if p)


def discover_phase(before: str, after: str, also_update: list[str],
                   md_filter: str, dry_run: bool = False) -> dict:
    print(f"\n[Phase 1] Discover updates needed between {before} and {after}")
    diff = collect_source_diff_summary(before, after)
    print(f"  source diff: {len(diff['commits'])} commits, "
          f"{len(diff['files_changed'])} files changed")
    if not diff["commits"]:
        if not also_update:
            raise RuntimeError(f"no commits between {before} and {after}; check the tags")
        print(f"  WARNING: no commits between {before} and {after}; only "
              f"--also-update pages are planned", file=sys.stderr)
    md_index = collect_md_index(md_filter)
    print(f"  docs index:  {len(md_index)} markdown file(s)")

    plan: dict = {
        "before": before,
        "after": after,
        # The update phase refuses a plan whose tags have moved since discovery.
        "before_commit": diff["before_commit"],
        "after_commit": diff["after_commit"],
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files_to_update": [],
        "llm_summary": "",
        "manual_overrides": [],
    }

    if not diff["commits"]:
        pass  # empty range: nothing to triage, only --also-update pages
    elif dry_run:
        print(f"  --dry-run: not asking OpenAI to triage {len(diff['commits'])} commits "
              f"against {len(md_index)} pages; the plan holds only --also-update pages")
    elif not os.getenv("OPENAI_API_KEY"):
        print("  WARNING: OPENAI_API_KEY not set — skipping LLM analysis. "
              "Plan will only contain --also-update entries (if any).")
    else:
        try:
            client = create_client()
        except RuntimeError as exc:
            print(f"  WARNING: {exc} — LLM analysis skipped.")
        else:
            user_text = build_discover_prompt(diff, md_index)
            print(f"  asking OpenAI ({DISCOVER_MODEL}) to triage...")
            try:
                parsed, usage = call_llm_streaming(
                    client, DISCOVER_SYSTEM, user_text,
                    DISCOVER_MAX_TOKENS, DISCOVER_MODEL,
                    "docs_discovery", DISCOVER_SCHEMA,
                )
            finally:
                client.close()
            print(f"  tokens: in={usage['input_tokens']} "
                  f"out={usage['output_tokens']} "
                  f"reasoning={usage['reasoning_tokens']}")
            plan["files_to_update"] = []
            for entry in parsed.get("files_to_update", []) or []:
                rel = plannable_path(entry.get("path", ""), "discovery")
                if rel:
                    plan["files_to_update"].append({**entry, "path": rel})
            plan["llm_summary"] = parsed.get("no_update_needed_summary", "") or ""

    # Attach diff_context for every LLM-discovered entry. Files added via
    # --also-update get diff_context = null so the update session does NOT
    # narrow its focus based on the source diff.
    for entry in plan["files_to_update"]:
        related = entry.get("related_source_files", []) or []
        reason = entry.get("reason", "")
        entry["diff_context"] = build_diff_context(diff, related, reason)

    if also_update:
        existing_paths = {e["path"] for e in plan["files_to_update"]}
        for path in also_update:
            path = plannable_path(path, "--also-update")
            if not path:
                continue
            plan["manual_overrides"].append(path)
            if path in existing_paths:
                # The path was already in the LLM-discovered list; keep the
                # diff_context that we built for it. Do NOT downgrade it to
                # null, because the diff context is genuine evidence.
                continue
            plan["files_to_update"].append({
                "path": path,
                "reason": "manual override (--also-update)",
                "related_source_files": [],
                "diff_context": None,
            })

    if dry_run:
        print("\n  (dry-run — plan not saved)")
    else:
        PLANS_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        plan_path = PLANS_DIR / f"plan_{ts}.json"
        plan_path.write_text(
            json.dumps(plan, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        plan["_plan_path"] = str(plan_path.relative_to(REPO_ROOT))
        print(f"\n  plan saved: {plan['_plan_path']}")
    print(f"  files to update: {len(plan['files_to_update'])}")
    if plan["manual_overrides"]:
        print(f"  manual overrides: {len(plan['manual_overrides'])}")
    return plan


# --- Source extraction (for Phase 2) ----------------------------------------

def _find_balanced(text: str, open_pos: int) -> int:
    open_c = text[open_pos]
    close_c = {"{": "}", "(": ")"}.get(open_c)
    if not close_c:
        return -1
    depth = 0
    in_str: str | None = None
    i = open_pos
    while i < len(text):
        c = text[i]
        if in_str:
            if c == "\\" and i + 1 < len(text):
                i += 2
                continue
            if c == in_str:
                in_str = None
        elif c == '"':
            in_str = c
        elif c == open_c:
            depth += 1
        elif c == close_c:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def find_command_handler_source(src_root: Path, command: str) -> dict | None:
    """Locate the C++ handler for `command`. Returns
    {file, registration_line, handler_function, handler_body} or None."""
    bare = command.split()[0].upper()
    grep_pat = rf'CI{{[^}}]*"{re.escape(bare)}"'
    p = run(["grep", "-rln", "-E", grep_pat, str(src_root / "src"),
             "--include=*.cc", "--include=*.h"], check=False)
    files = [Path(line) for line in p.stdout.splitlines() if line]
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # find registration: CI{ "BARE", ... }.HFUNC(<func>) — broadly
        reg_re = re.compile(
            rf'CI{{[^}}]*"{re.escape(bare)}"[^}}]*}}\s*\.\s*'
            r'(?:HFUNC|MFUNC|HFUNC2|SetHandler)\s*\(\s*(?P<fn>[A-Za-z_]\w*)',
            re.DOTALL,
        )
        rm = reg_re.search(text)
        if not rm:
            continue
        fn_name = rm.group("fn")
        candidates = [f"Cmd{fn_name}", fn_name]
        for cand in candidates:
            body_re = re.compile(
                r"(?:^|\n)\s*(?:[A-Za-z_][\w<>:&*]*\s+)+"
                r"(?:[A-Za-z_]\w*::)?" + re.escape(cand)
                + r"\s*\([^{};]*?\)\s*(?:const|noexcept)?\s*\{",
                re.DOTALL,
            )
            bm = body_re.search(text)
            if not bm:
                continue
            open_brace = bm.end() - 1
            close_brace = _find_balanced(text, open_brace)
            if close_brace > open_brace:
                body = text[bm.start():close_brace + 1]
                if len(body) > 8000:
                    body = body[:8000] + "\n// ... (truncated)\n}"
                return {
                    "file": str(f.relative_to(src_root)),
                    "registration_line": text[:rm.start()].count("\n") + 1,
                    "handler_function": cand,
                    "handler_body": body,
                }
    return None


# --- MDX safety net (forbid raw <placeholder> JSX-confusable angle brackets) -

# Common HTML elements that Docusaurus / MDX 3 accept as-is when the page
# uses them deliberately (e.g. `<details><summary>...</summary></details>`
# blocks, inline `<code>...</code>`, `<b>`, etc.). We only consider these
# "safe" — every OTHER lowercase `<tag>` is treated as a placeholder that
# would crash the build.
KNOWN_HTML_TAGS = frozenset({
    "a", "abbr", "address", "article", "aside", "b", "blockquote", "br",
    "button", "cite", "code", "col", "colgroup", "dd", "del", "details",
    "div", "dl", "dt", "em", "figcaption", "figure", "footer", "h1", "h2",
    "h3", "h4", "h5", "h6", "header", "hr", "i", "img", "input", "ins",
    "kbd", "label", "li", "main", "mark", "nav", "noscript", "ol", "p",
    "pre", "s", "samp", "section", "small", "span", "strong", "sub",
    "summary", "sup", "table", "tbody", "td", "tfoot", "th", "thead",
    "time", "tr", "u", "ul", "var", "wbr",
})

_FENCE_RE = re.compile(r"^\s*(```|~~~)")
_INDENTED_RE = re.compile(r"^( {4,}|\t)")
_PLACEHOLDER_RE = re.compile(r"<([a-z][a-z0-9_:.\-]*)>")
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def _wrap_placeholders_in_prose(line: str) -> str:
    """Wrap bare `<placeholder>` in inline code, preserving content already
    inside backtick spans and leaving known HTML tags alone."""
    def sub_outside_code(s: str) -> str:
        return _PLACEHOLDER_RE.sub(
            lambda m: m.group(0)
            if m.group(1).lower() in KNOWN_HTML_TAGS
            else f"`<{m.group(1)}>`",
            s,
        )
    out: list[str] = []
    last = 0
    for m in _INLINE_CODE_RE.finditer(line):
        out.append(sub_outside_code(line[last:m.start()]))
        out.append(m.group(0))
        last = m.end()
    out.append(sub_outside_code(line[last:]))
    return "".join(out)


def fix_mdx_jsx_unsafe(text: str) -> str:
    """Make `text` safe for MDX 3 parsing.

    MDX 3 treats `<word>` as JSX even inside indented code blocks, so a
    bare `<key>` placeholder breaks the site build. Strategy:
      * Inside fenced ``` ... ``` blocks: leave content untouched.
      * Inside 4-space indented blocks that contain placeholders: convert
        the whole block to a fenced ```text``` block (safe).
      * In prose: wrap `<word>` placeholders in inline code (`` `<word>` ``)
        unless `word` is a known HTML element or already inside an existing
        backtick span.
    """
    lines = text.splitlines()
    out: list[str] = []
    in_fence = False
    i = 0
    while i < len(lines):
        line = lines[i]
        if _FENCE_RE.match(line):
            in_fence = not in_fence
            out.append(line)
            i += 1
            continue
        if not in_fence and _INDENTED_RE.match(line):
            j = i
            block: list[str] = []
            while j < len(lines):
                ln = lines[j]
                if _FENCE_RE.match(ln):
                    break
                if ln.strip() == "" or _INDENTED_RE.match(ln):
                    block.append(ln)
                    j += 1
                else:
                    break
            while block and block[-1].strip() == "":
                block.pop()
            if any(_PLACEHOLDER_RE.search(b) for b in block):
                stripped = [b[4:] if b.startswith("    ") else b.lstrip("\t")
                            for b in block]
                out.append("```text")
                out.extend(stripped)
                out.append("```")
                i = i + len(block)
                continue
            out.extend(block)
            i = i + len(block)
            continue
        if not in_fence:
            line = _wrap_placeholders_in_prose(line)
        out.append(line)
        i += 1
    result = "\n".join(out)
    if text.endswith("\n") and not result.endswith("\n"):
        result += "\n"
    return result


# --- Docker example verification --------------------------------------------

SHELL_BLOCK_RE = re.compile(
    # The closing fence must not consume the newline after it: rebuilt blocks
    # end at the fence, so the blank line that follows would be lost.
    r"^```shell[ \t]*\n(?P<body>.*?)^```[ \t]*$",
    re.DOTALL | re.MULTILINE,
)
PROMPT = "dragonfly> "
CLI_PREFIX = "$ redis-cli "

# A whole block runs in one redis-cli session, so all replies arrive on one
# stream. After each command the harness sends this unknown command; Dragonfly
# answers `(error) ERR unknown command `__DOCSYNC_SEP_<n>__`` (it upper-cases
# the name), also after HELLO 3 and for a user with -@all. The marker replies
# split the stream per command.
REPLY_MARKER = "__DOCSYNC_SEP_{}__"
REPLY_MARKER_RE = re.compile(r"^\(error\) ERR unknown command\b.*?__DOCSYNC_SEP_(\d+)__",
                             re.IGNORECASE)
# In a session redis-cli prints how long a command took when it took 0.5 s or
# more, e.g. `(1.00s)` after `BLPOP k 1`. A one-shot call does not print it.
TIMING_LINE_RE = re.compile(r"^\(\d+\.\d\ds\)$")
# A server error reply, at top level or nested in an array reply (EXEC).
ERROR_REPLY_RE = re.compile(r"^[ \t]*(?:\d+[)#][ \t]+)*\(error\)[ \t]")
# redis-cli's own answer to a line it cannot parse (an unbalanced quote).
CLI_PARSE_ERROR = "Invalid argument(s)"
# Inside MULTI the server answers each command with one line, QUEUED or a
# queue-time error. These commands run at once instead and end the
# transaction: EXEC/DISCARD (the exec group) and RESET (main_service.cc). No
# marker is sent inside MULTI: the server rejects an unknown command there and
# EXEC then fails with EXECABORT.
MULTI_ENDERS = frozenset({"DISCARD", "EXEC", "RESET"})
# redis-cli handles these itself: it exits without sending them, so the
# session ends there and no reply marker follows.
REDIS_CLI_EXIT_COMMANDS = frozenset({"EXIT", "QUIT"})
# Bounds for the `docker` calls of the example harness. BLOCK_TIMEOUT_S bounds
# one block (one redis-cli session) or one `$ redis-cli` line. coreutils
# `timeout` enforces it inside the container: killing only the local docker
# CLI would leave a blocked redis-cli in the container, consuming data that
# later examples push. The host-side limit is a backstop.
BLOCK_TIMEOUT_S = 30
KILL_AFTER_S = 5
HOST_GRACE_S = 15
PROBE_TIMEOUT_S = 5
DOCKER_RUN_TIMEOUT_S = 120
DOCKER_RM_TIMEOUT_S = 60


FENCED_BLOCK_RE = re.compile(r"^```[^\n]*\n(?P<body>.*?)^```[ \t]*$", re.DOTALL | re.MULTILINE)
EXAMPLE_PROMPTS = ("dragonfly> ", "dragonfly$> ")


def example_commands(text: str) -> Counter:
    """Every `dragonfly>` / `dragonfly$>` command line in any fenced block."""
    out: Counter = Counter()
    for m in FENCED_BLOCK_RE.finditer(text):
        for line in m.group("body").splitlines():
            line = line.strip()
            if line.startswith(EXAMPLE_PROMPTS):
                out[line] += 1
    return out


def prose_lines(text: str) -> list[str]:
    """Non-blank lines outside the front matter and fenced blocks."""
    body = FRONTMATTER_RE.sub("", text, count=1)
    body = FENCED_BLOCK_RE.sub("", body)
    return [line.strip() for line in body.splitlines() if line.strip()]


def removed_prose(input_md: str, output_md: str) -> list[str]:
    """Prose lines of the input that the output no longer contains verbatim:
    removed or rewritten text a human should check."""
    kept = Counter(prose_lines(output_md))
    removed = []
    for line in prose_lines(input_md):
        if kept[line]:
            kept[line] -= 1
        else:
            removed.append(line)
    return removed


def extract_redis_invocations(text: str) -> list[str]:
    """Return every `dragonfly>` line found inside ```shell blocks."""
    invocations: list[str] = []
    for m in SHELL_BLOCK_RE.finditer(text):
        for line in m.group("body").splitlines():
            line = line.rstrip()
            if line.startswith(PROMPT):
                invocations.append(line[len(PROMPT):].strip())
            elif line.startswith(CLI_PREFIX):
                invocations.append(line[len(CLI_PREFIX):].strip())
    return invocations


def block_lines(match: re.Match) -> list[str]:
    return match.group("body").rstrip("\n").split("\n")


def block_commands(lines: list[str]) -> list[str]:
    """The `dragonfly>` commands of a block, in order."""
    return [line[len(PROMPT):].strip() for line in lines if line.startswith(PROMPT)]


def block_cli_lines(lines: list[str]) -> list[str]:
    """The `$ redis-cli` lines of a block, without the prefix."""
    return [line[len(CLI_PREFIX):].strip() for line in lines if line.startswith(CLI_PREFIX)]


class DockerTimeout(RuntimeError):
    """The host-side limit on a `docker` call fired. The process in the
    container may still be running, so the container must not be reused."""


class ExampleRunError(RuntimeError):
    """A changed or new example block did not run to completion, so its
    output is unknown and the page must not be written."""


@dataclass
class SessionRun:
    stdout: str
    stderr: str
    returncode: int
    timed_out: bool  # the in-container `timeout` ended redis-cli


def _decode(data: bytes | str | None) -> str:
    """Text as subprocess's text mode gives it: UTF-8, universal newlines."""
    if data is None:
        return ""
    text = data.decode("utf-8", errors="replace") if isinstance(data, bytes) else data
    return text.replace("\r\n", "\n").replace("\r", "\n")


@dataclass
class DockerSession:
    container: str
    tag: str

    def _redis_cli(self, stdin: bool) -> list[str]:
        return (["docker", "exec"] + (["-i"] if stdin else []) + [
            self.container, "timeout", "-k", str(KILL_AFTER_S), str(BLOCK_TIMEOUT_S),
            "redis-cli", "--no-raw"])

    def _run(self, cmd: list[str], stdin: str | None = None) -> SessionRun:
        limit = BLOCK_TIMEOUT_S + KILL_AFTER_S + HOST_GRACE_S
        try:
            p = subprocess.run(cmd, input=None if stdin is None else stdin.encode("utf-8"),
                               capture_output=True, timeout=limit)
        except subprocess.TimeoutExpired:
            raise DockerTimeout(
                f"`docker exec {self.container} ... redis-cli` did not finish in {limit} s "
                f"although redis-cli runs under `timeout {BLOCK_TIMEOUT_S}` in the container"
            ) from None
        # timeout(1) exits 124 after SIGTERM and 137 after the SIGKILL that -k sends.
        return SessionRun(_decode(p.stdout), _decode(p.stderr), p.returncode,
                          p.returncode in (124, 137))

    def exec(self, argv: list[str]) -> tuple[str, str, int | None]:
        """One redis-cli call with `argv` (used for `$ redis-cli` lines).
        Returns (stdout, stderr, returncode); returncode is None on a timeout."""
        run = self._run(self._redis_cli(stdin=False) + argv)
        stderr = run.stderr.rstrip()
        if run.timed_out:
            stderr = "\n".join(filter(None, [stderr, f"timed out after {BLOCK_TIMEOUT_S} s"]))
        return run.stdout.rstrip(), stderr, None if run.timed_out else run.returncode

    def run_session(self, script: str) -> SessionRun:
        """Feed `script` to one interactive redis-cli on stdin. redis-cli parses
        each line itself (quotes, \\x escapes), as for a reader typing it."""
        return self._run(self._redis_cli(stdin=True), stdin=script)


def remove_container(container: str) -> None:
    try:
        subprocess.run(["docker", "rm", "-f", container], capture_output=True,
                       timeout=DOCKER_RM_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        print(f"  WARNING: `docker rm -f {container}` did not finish in "
              f"{DOCKER_RM_TIMEOUT_S} s; remove the container by hand", file=sys.stderr)


def boot_docker(tag: str, emulated_cluster: bool = False) -> DockerSession:
    """Boot the local image; update_phase has already pulled and verified it."""
    image_ref = f"{DRAGONFLY_IMAGE}:{tag}"
    container = f"dfly-docs-sync-{tag.replace('.', '-')}-{os.getpid()}"
    args = ["docker", "run", "-d", "--pull=never", "--name", container, image_ref]
    if emulated_cluster:
        args.append("--cluster_mode=emulated")
    try:
        run(args, timeout=DOCKER_RUN_TIMEOUT_S)
    except subprocess.TimeoutExpired:
        remove_container(container)
        raise RuntimeError(f"`docker run` of {image_ref} did not finish in "
                           f"{DOCKER_RUN_TIMEOUT_S} s") from None
    deadline = time.time() + PING_TIMEOUT_S
    while time.time() < deadline:
        # The probe also checks that the image has `timeout`, which every
        # example run relies on.
        try:
            p = run(["docker", "exec", container, "timeout", str(PROBE_TIMEOUT_S),
                     "redis-cli", "PING"], check=False,
                    timeout=PROBE_TIMEOUT_S + HOST_GRACE_S)
        except subprocess.TimeoutExpired:
            continue
        if p.returncode == 0 and "PONG" in p.stdout:
            return DockerSession(container=container, tag=tag)
        if p.returncode in (126, 127):
            remove_container(container)
            raise RuntimeError(f"{image_ref} cannot run `timeout ... redis-cli`: "
                               f"{(p.stderr or p.stdout).strip()}")
        time.sleep(0.3)
    remove_container(container)
    raise RuntimeError(f"Dragonfly {tag} did not respond to PING")


def kill_docker(session: DockerSession) -> None:
    remove_container(session.container)


def tokenize_invocation(cmd: str) -> list[str]:
    """Split a `dragonfly>` command line into redis-cli argv.

    Uses shell-style tokenization (shlex) so quoted values are unquoted the
    way a shell / the redis-cli REPL would handle them — e.g.
    `HSETEX k 30 user "alice"` yields the value `alice`, not the literal
    `"alice"` (which the server would store with the quotes, rendering as
    `"\\"alice\\""` under --no-raw). Falls back to a plain whitespace split
    if the line is not valid shell syntax (e.g. an unbalanced quote), so a
    malformed example degrades to the old behaviour instead of raising.

    Used for `$ redis-cli` lines and to read command names. `dragonfly>`
    lines are sent to redis-cli verbatim instead (run_example_block).
    """
    try:
        return shlex.split(cmd)
    except ValueError:
        return cmd.split()


def command_name(command: str) -> str:
    argv = tokenize_invocation(command)
    return argv[0].upper() if argv else ""


TOPOLOGY_DEPENDENT_COMMANDS = frozenset({
    "ASKING",
    "CLUSTER",
    "DFLYCLUSTER",
    "DFLYMIGRATE",
    "FAILOVER",
    "MIGRATE",
    "PSYNC",
    "READONLY",
    "READWRITE",
    "REPLCONF",
    "REPLICAOF",
    "REPLTAKEOVER",
    "ROLE",
    "SENTINEL",
    "SLAVEOF",
    "SYNC",
    "WAIT",
    "WAITAOF",
})

# Commands after which redis-cli waits for pushed messages and never reads the
# next line, so a session that contains them never ends.
PUSH_MODE_COMMANDS = frozenset({"MONITOR", "PSUBSCRIBE", "SSUBSCRIBE", "SUBSCRIBE"})

REDIS_CLI_OPTIONS_WITH_VALUE = frozenset({
    "--cacert",
    "--cacertdir",
    "--cert",
    "--key",
    "--pass",
    "--sni",
    "--user",
    "--uri",
    "-a",
    "-h",
    "-n",
    "-p",
    "-s",
    "-u",
})


def strip_redis_cli_options(argv: list[str]) -> list[str]:
    """Return command arguments from a `$ redis-cli [options] COMMAND` line."""
    index = 0
    while index < len(argv) and argv[index].startswith("-"):
        option = argv[index]
        option_name = option.split("=", 1)[0]
        index += 1
        if option_name in REDIS_CLI_OPTIONS_WITH_VALUE and "=" not in option:
            index += 1
    return argv[index:]


def topology_skip_reason(invocation: str) -> str | None:
    """Explain why an example cannot be verified in the default container.

    A single Dragonfly process, even in emulated cluster mode, cannot reproduce
    replica acknowledgements, native-cluster slot migration, remote-node state,
    or failover. Replacing curated output with that process's response corrupts
    otherwise valid examples.
    """
    argv = strip_redis_cli_options(tokenize_invocation(invocation))
    if not argv:
        return None

    command = argv[0].upper()
    if command == "CLUSTER" and len(argv) > 1 and argv[1].upper() in {"HELP", "KEYSLOT"}:
        return None
    if command in TOPOLOGY_DEPENDENT_COMMANDS:
        return f"{command} requires configured replication, cluster, or remote-node state"

    info_sections = {arg.upper() for arg in argv[1:]}
    if command == "INFO" and (
        not info_sections
        or "DEFAULT" in info_sections
        or bool(info_sections & {"ALL", "CLUSTER", "REPLICATION"})
    ):
        return "INFO output depends on configured replication or cluster state"

    return None


def push_mode_skip_reason(invocation: str) -> str | None:
    """Explain why an example would never finish in a redis-cli session."""
    argv = strip_redis_cli_options(tokenize_invocation(invocation))
    if argv and argv[0].upper() in PUSH_MODE_COMMANDS:
        return (f"{argv[0].upper()} switches the connection to push mode: redis-cli "
                "then waits for messages and never returns")
    return None


def block_skip(invocations: list[str]) -> tuple[str, str] | None:
    """(kind, reason) when a block is kept as written instead of being run:
    kind is "topology" or "push-mode"."""
    for kind, check in (("topology", topology_skip_reason),
                        ("push-mode", push_mode_skip_reason)):
        for invocation in invocations:
            reason = check(invocation)
            if reason:
                return kind, reason
    return None


# --- One redis-cli session per block -------------------------------------------

@dataclass(frozen=True)
class SessionStep:
    command: str
    marker: int | None  # reply marker sent after the command; None inside MULTI


@dataclass(frozen=True)
class SessionPlan:
    steps: tuple[SessionStep, ...]
    terminal: int | None = None  # extra marker when the block ends inside MULTI

    def script(self) -> str:
        lines: list[str] = []
        for step in self.steps:
            lines.append(step.command)
            if step.marker is not None:
                lines.append(REPLY_MARKER.format(step.marker))
        if self.terminal is not None:
            lines.append(REPLY_MARKER.format(self.terminal))
        return "\n".join(lines) + "\n"


@dataclass
class SessionSplit:
    outputs: list[str]               # one reply per completed step, in order
    failed_step: int | None = None   # step whose reply could not be told apart
    failure: str | None = None


def plan_session(commands: list[str], flush: bool = True) -> SessionPlan:
    """The redis-cli input for one block: FLUSHALL (if `flush`), then each
    command line verbatim, each followed by a reply marker except inside MULTI."""
    steps: list[SessionStep] = []
    marker = 0
    in_multi = False
    for command in (["FLUSHALL"] if flush else []) + list(commands):
        name = command_name(command)
        if in_multi and name in MULTI_ENDERS:
            in_multi = False
        elif in_multi or name == "MULTI":
            in_multi = True
            steps.append(SessionStep(command, None))
            continue
        steps.append(SessionStep(command, marker))
        marker += 1
    return SessionPlan(tuple(steps), marker if in_multi else None)


def split_session_output(stdout: str, plan: SessionPlan) -> SessionSplit:
    """Split one session's stdout into the reply of each step of `plan`.

    A step followed by a marker owns every line up to that marker's reply. A
    step inside MULTI owns exactly one line. Stops at the first step whose
    reply cannot be told apart and names it in `failure`."""
    lines = stdout.split("\n")
    if lines and lines[-1] == "":
        lines.pop()
    pos = 0
    outputs: list[str] = []
    in_multi = False

    def marker_at(index: int) -> int | None:
        m = REPLY_MARKER_RE.match(lines[index]) if index < len(lines) else None
        return int(m.group(1)) if m else None

    for index, step in enumerate(plan.steps):
        name = command_name(step.command)
        if step.marker is None:
            if pos >= len(lines):
                return SessionSplit(outputs, index, f"no reply to `{step.command}`")
            if marker_at(pos) is not None:
                return SessionSplit(outputs, index,
                                    f"a reply marker came where `{step.command}` should reply")
            line = lines[pos]
            pos += 1
            if name == "MULTI" and not in_multi:
                if line != "OK":
                    return SessionSplit(
                        outputs, index,
                        f"`{step.command}` replied {line!r}, not OK, so the commands after "
                        "it were not queued and their replies cannot be told apart")
                in_multi = True
            elif line != "QUEUED" and not line.startswith("(error)"):
                return SessionSplit(
                    outputs, index,
                    f"`{step.command}` replied {line!r} inside MULTI, not QUEUED or an error")
            outputs.append(line)
            continue
        segment: list[str] = []
        while pos < len(lines) and marker_at(pos) is None:
            segment.append(lines[pos])
            pos += 1
        if pos >= len(lines):
            return SessionSplit(outputs, index, f"no reply marker after `{step.command}`")
        got = marker_at(pos)
        pos += 1
        if got != step.marker:
            return SessionSplit(outputs, index, f"reply marker {got} came after "
                                                f"`{step.command}`, expected {step.marker}")
        if segment and TIMING_LINE_RE.match(segment[-1]):
            segment.pop()
        outputs.append("\n".join(segment).rstrip())
        if name in MULTI_ENDERS:
            in_multi = False
    if plan.terminal is not None:
        if marker_at(pos) != plan.terminal:
            return SessionSplit(outputs, len(plan.steps),
                                "no reply marker at the end of the block")
        pos += 1
    trailing = [line for line in lines[pos:] if line.strip()]
    if trailing:
        return SessionSplit(outputs, len(plan.steps),
                            f"unexpected output after the last reply marker: {trailing[:3]}")
    return SessionSplit(outputs)


def error_reply(output: str) -> str | None:
    """The first server error line of a reply, or redis-cli's parse error."""
    for line in output.split("\n"):
        if ERROR_REPLY_RE.match(line):
            return line.strip()
    if output.strip() == CLI_PARSE_ERROR:
        return CLI_PARSE_ERROR
    return None


@dataclass
class BlockRun:
    outputs: list[str]   # trusted replies of the block's commands, in order
    failure: str | None  # why the block did not complete or cannot be trusted


def run_example_block(session: DockerSession, commands: list[str]) -> BlockRun:
    """FLUSHALL, then the block's command lines, in one redis-cli session.

    `outputs` keeps the replies before the step that failed. It keeps none
    when FLUSHALL did not reply OK (an earlier example set requirepass or
    turned the default user off, so every reply is NOAUTH), when redis-cli
    wrote to stderr (it lost the connection, e.g. on CLIENT KILL of its own
    address, dropped that reply and went on in a new connection without the
    block's state) or when it exited non-zero. Raises DockerTimeout when the
    host-side backstop fires."""
    plan = plan_session(commands, flush=True)
    session_run = session.run_session(plan.script())
    split = split_session_output(session_run.stdout, plan)
    outputs = split.outputs[1:]
    flush_reply = split.outputs[0] if split.outputs else None
    failure = split.failure
    stderr = session_run.stderr.strip()
    if session_run.timed_out:
        stuck = (plan.steps[split.failed_step].command
                 if split.failed_step is not None and split.failed_step < len(plan.steps)
                 else None)
        failure = (f"timed out after {BLOCK_TIMEOUT_S} s"
                   + (f": `{stuck}` did not return" if stuck else ""))
    elif failure is None:
        if flush_reply != "OK":
            failure = (f"FLUSHALL before the block replied {flush_reply!r}, not OK, so the "
                       "block did not start from an empty keyspace")
        elif stderr:
            failure = ("redis-cli reported a connection error: a reply may be missing and "
                       "the commands after it may have run in a new connection")
        elif session_run.returncode != 0:
            failure = f"redis-cli exited with status {session_run.returncode}"
        if failure:
            outputs = []
    if stderr:
        # redis-cli retries a command whose connection broke in a new
        # connection and reports only a failed retry, so the reply that broke
        # cannot be told from the ones that followed it.
        outputs = []
    if (failure and split.failed_step is not None and split.failed_step < len(plan.steps)
            and command_name(plan.steps[split.failed_step].command) in REDIS_CLI_EXIT_COMMANDS):
        failure += " (redis-cli exits on QUIT and EXIT without sending them to the server)"
    if failure and stderr:
        failure += f" (redis-cli stderr: {' | '.join(stderr.splitlines()[:3])})"
    return BlockRun(outputs, failure)


def observe_examples(session: DockerSession, text: str) -> tuple[list[dict], list[str]]:
    """Run the page's current examples before the LLM call, block by block
    with the rules of verify_and_substitute_examples, and return
    (observations, notes). A block that does not complete is reported
    (`not_run`, `failure`) and the next block still runs: the in-container
    timeout has already ended its redis-cli. `$ redis-cli` lines run as
    separate calls after the block's session. Raises DockerTimeout."""
    observations: list[dict] = []
    commands_run = blocks_run = 0
    error_replies: list[str] = []
    incomplete: list[str] = []
    for number, m in enumerate(SHELL_BLOCK_RE.finditer(text), 1):
        lines = block_lines(m)
        commands = block_commands(lines)
        cli_lines = block_cli_lines(lines)
        invocations = commands + [CLI_PREFIX + inv for inv in cli_lines]
        skip = block_skip(commands + cli_lines)
        if skip:
            observations.extend({"block": number, "invocation": inv, "skipped": True,
                                 "skip_reason": skip[1]} for inv in invocations)
            continue
        if commands:
            blocks_run += 1
            block_run = run_example_block(session, commands)
            for index, command in enumerate(commands):
                if index >= len(block_run.outputs):
                    observations.append({"block": number, "invocation": command,
                                         "not_run": True, "failure": block_run.failure})
                    continue
                output = block_run.outputs[index]
                reply = error_reply(output)
                observations.append({"block": number, "invocation": command,
                                     "output": output, "error_reply": bool(reply)})
                commands_run += 1
                if reply:
                    error_replies.append(f"block {number}: {command} -> {reply}")
            if block_run.failure:
                incomplete.append(f"block {number}: {block_run.failure}")
        for inv in cli_lines:
            stdout, stderr, rc = session.exec(tokenize_invocation(inv))
            output = stdout if stdout else stderr
            observations.append({"block": number, "invocation": CLI_PREFIX + inv,
                                 "output": output, "returncode": rc,
                                 "error_reply": bool(error_reply(output)) or rc != 0})
    notes: list[str] = []
    if blocks_run:
        notes.append(f"ran the page's current examples before the LLM call: {commands_run} "
                     f"`dragonfly>` invocation(s) in {blocks_run} block(s), one redis-cli "
                     "session per block (FLUSHALL first)")
    if error_replies:
        notes.append(f"current examples gave {len(error_replies)} error repl(ies): "
                     + "; ".join(error_replies[:5]) + ("; ..." if len(error_replies) > 5 else ""))
    if incomplete:
        notes.append("current example block(s) that did not complete: " + "; ".join(incomplete))
    return observations, notes


def normalize_for_compare(text: str) -> list[str]:
    """Reduce text to the sequence of its non-blank lines, with each line's
    trailing whitespace stripped but internal whitespace preserved.

    Two texts that compare equal under this normalization differ ONLY in
    blank-line counts and/or trailing-whitespace — i.e. they are
    semantically identical. Real edits change at least one non-blank line.
    """
    return [l.rstrip() for l in text.split("\n") if l.strip()]


# Any ACL metadata line, also a qualified one such as
# `**ACL categories (Dragonfly v2.0.2):**`. acl_sync.py owns them all.
ACL_LINE_LOOSE_RE = re.compile(r"^[ \t]*[\-*]?[ \t]*\*\*ACL[ \t]+categor[^\n]*$",
                               re.MULTILINE | re.IGNORECASE)


def validate_update_output(input_md: str, output_md: str) -> list[str]:
    """Structural sanity check between LLM output and the input page.
    Returns list of error strings (empty = pass).

    These checks catch catastrophic LLM failures like returning `...`,
    truncating mid-document, or losing the frontmatter / H1 / required
    JSX imports. We do NOT call validation a soft warning — anything
    here means we refuse to write the file.
    """
    errors: list[str] = []

    if len(output_md.strip()) < 80:
        errors.append(
            f"output is catastrophically short "
            f"({len(output_md.strip())} non-whitespace chars; "
            f"input was {len(input_md)})"
        )
    elif len(output_md) < len(input_md) * 0.5:
        errors.append(
            f"output ({len(output_md)} chars) shrunk to less than half "
            f"of input ({len(input_md)} chars) — likely truncation"
        )

    if re.match(r"\A\s*\.{3,}\s*\Z", output_md):
        errors.append("output is a placeholder (`...`)")

    in_fm = bool(re.match(r"\A---\n.*?\n---\n", input_md, re.DOTALL))
    out_fm = bool(re.match(r"\A---\n.*?\n---\n", output_md, re.DOTALL))
    if in_fm and not out_fm:
        errors.append("frontmatter (---...---) block was lost")
    elif in_fm:
        in_front = FRONTMATTER_RE.match(input_md).group(0)
        out_front = FRONTMATTER_RE.match(output_md)
        if not out_front or out_front.group(0) != in_front:
            errors.append("frontmatter was changed; it must stay byte-identical")

    # Existing examples may get setup lines and new commands, but no existing
    # command may disappear: a command that fails in isolation needs setup, not
    # removal, and a replaced example loses what a human chose to show.
    dropped = example_commands(input_md) - example_commands(output_md)
    if dropped:
        listed = "; ".join(sorted(dropped)[:5]) + ("; ..." if len(dropped) > 5 else "")
        errors.append(f"{sum(dropped.values())} existing example command(s) were removed "
                      f"or changed: {listed}")

    if re.search(r"^# ", input_md, re.MULTILINE) \
            and not re.search(r"^# ", output_md, re.MULTILINE):
        errors.append("H1 header was lost")

    in_h2 = len(re.findall(r"^## ", input_md, re.MULTILINE))
    out_h2 = len(re.findall(r"^## ", output_md, re.MULTILINE))
    if out_h2 < in_h2:
        errors.append(
            f"H2 section count dropped from {in_h2} to {out_h2} — "
            f"page structure was changed"
        )

    if "<PageTitle" in input_md and "<PageTitle" not in output_md:
        errors.append("<PageTitle ...> tag was lost")

    if "import PageTitle" in input_md and "import PageTitle" not in output_md:
        errors.append("`import PageTitle from ...` line was lost")

    # A standalone container cannot validate these examples, and a redis-cli
    # session never ends on a push-mode command. Require the LLM to preserve
    # every such existing shell block byte-for-byte.
    for match in SHELL_BLOCK_RE.finditer(input_md):
        block = match.group(0)
        skip = block_skip(extract_redis_invocations(block))
        if skip and block not in output_md:
            if skip[0] == "topology":
                errors.append(
                    "topology-dependent shell block was modified without a "
                    "topology-specific runtime fixture"
                )
            else:
                errors.append(
                    "push-mode shell block (SUBSCRIBE, PSUBSCRIBE, SSUBSCRIBE or "
                    "MONITOR) was modified; it cannot be run in a redis-cli session"
                )

    # ACL lines: rule #4 says do not modify, remove or add one. Every ACL-like
    # input line must appear verbatim in the output, and the output may not
    # have ACL-like lines the input does not have.
    in_acl = Counter(line.rstrip() for line in ACL_LINE_LOOSE_RE.findall(input_md))
    out_acl = Counter(line.rstrip() for line in ACL_LINE_LOOSE_RE.findall(output_md))
    for line in (in_acl - out_acl):
        errors.append(
            f"ACL categories line was modified or removed (rule #4 — owned by "
            f"acl_sync.py): {line.strip()!r}"
        )
    for line in (out_acl - in_acl):
        errors.append(
            f"ACL categories line was added (rule #4 — owned by acl_sync.py): "
            f"{line.strip()!r}"
        )

    return errors


def classify_blocks(text: str,
                    baseline_text: str | None = None) -> list[tuple[int, re.Match, str]]:
    """(number, match, kind) for each ```shell block of `text`, numbered from 1.

    kind is "topology" or "push-mode" (kept as written: a standalone container
    cannot verify the block, or redis-cli never returns from it), "unchanged"
    (identical to the block at the same position in `baseline_text`),
    "no-commands" (no `dragonfly>` line) or "changed"."""
    baseline_blocks = (
        [match.group(0) for match in SHELL_BLOCK_RE.finditer(baseline_text)]
        if baseline_text is not None else []
    )
    blocks: list[tuple[int, re.Match, str]] = []
    for index, m in enumerate(SHELL_BLOCK_RE.finditer(text)):
        lines = block_lines(m)
        commands = block_commands(lines)
        skip = block_skip(commands + block_cli_lines(lines))
        if skip:
            kind = skip[0]
        elif index < len(baseline_blocks) and m.group(0) == baseline_blocks[index]:
            kind = "unchanged"
        elif not commands:
            kind = "no-commands"
        else:
            kind = "changed"
        blocks.append((index + 1, m, kind))
    return blocks


def unverified_new_blocks(text: str, baseline_text: str) -> list[dict]:
    """Topology-dependent and push-mode blocks of `text` that `baseline_text`
    does not have: they are never run, so their output is as the LLM wrote it."""
    out: list[dict] = []
    for number, m, kind in classify_blocks(text, baseline_text):
        if kind in ("topology", "push-mode") and m.group(0) not in baseline_text:
            invocations = extract_redis_invocations(m.group(0))
            out.append({"block": number, "kind": kind,
                        "command": invocations[0] if invocations else ""})
    return out


def kept_separator_lines(predicted: list[str], actual: list[str]) -> list[str]:
    """The blank and `#` comment lines that end the predicted output of a
    command: the page's spacing and comments before the next command, kept
    when the output is replaced. A `#` line that the actual output also has
    (an INFO section header) is output, not a comment."""
    actual_lines = set(actual)
    start = len(predicted)
    while start and (not predicted[start - 1].strip()
                     or (predicted[start - 1].lstrip().startswith("#")
                         and predicted[start - 1] not in actual_lines)):
        start -= 1
    return predicted[start:]


def verify_and_substitute_examples(
    text: str, session: DockerSession, baseline_text: str | None = None,
) -> tuple[str, list[dict], list[str]]:
    """Run every changed or new ```shell``` block in Docker and replace the
    lines after each `dragonfly>` line with the server's reply. Returns
    (new_text, errors, notes).

    Each block runs in ONE redis-cli session that starts with `FLUSHALL`:
    keys never leak from one block into the next, and connection state
    (SELECT, AUTH, HELLO 3, MULTI/EXEC, CLIENT settings) carries from line to
    line inside a block, as for a reader who types the block into redis-cli.
    Server state that FLUSHALL keeps (ACL users, CONFIG SET, scripts) carries
    into later blocks, as for that reader: unchanged blocks before the last
    changed one are replayed in page order for it, and their text is kept.
    Give a session whose server has not run this page's examples yet.

    Blocks unchanged from `baseline_text` (compared by position) are
    preserved to avoid churn from dynamic values and nondeterministic reply
    ordering. Blocks containing topology-dependent commands are also
    preserved verbatim: a single container cannot authoritatively verify
    replication, failover, or native-cluster output. So are blocks with
    SUBSCRIBE, PSUBSCRIBE, SSUBSCRIBE or MONITOR, which never return.

    In a rebuilt block each command's predicted output is replaced; blank
    and `#` comment lines that end it (spacing and comments before the next
    command) are kept.

    `errors` lists every reply that is a server error (or redis-cli's parse
    error) as {block, command, reply}, `block` being the 1-based number of the
    ```shell block. Those replies are still written: a page may document an
    error case. `notes` is a flat list of human-readable strings.

    Raises ExampleRunError when a changed block does not complete or cannot
    be trusted (timeout, a reply marker that never came, FLUSHALL refused, a
    lost connection), and DockerTimeout when the host-side limit fires: the
    caller must not write the page.
    """
    errors: list[dict] = []
    notes: list[str] = []
    out_parts: list[str] = []
    last_pos = 0
    invocation_count = 0
    block_count = 0
    kept = {"topology": 0, "push-mode": 0}
    new_kept: list[int] = []
    unchanged_block_count = 0
    replayed = 0
    replay_failures: list[str] = []
    blocks = classify_blocks(text, baseline_text)
    last_changed = max((number for number, _m, kind in blocks if kind == "changed"),
                       default=0)

    for number, m, kind in blocks:
        out_parts.append(text[last_pos:m.start()])
        last_pos = m.end()
        lines = block_lines(m)
        commands = block_commands(lines)
        if kind != "changed":
            out_parts.append(m.group(0))
            if kind in kept:
                kept[kind] += 1
                if baseline_text is not None and m.group(0) not in baseline_text:
                    new_kept.append(number)
            elif kind == "unchanged":
                unchanged_block_count += 1
                if commands and number < last_changed:
                    replay = run_example_block(session, commands)
                    replayed += 1
                    if replay.failure:
                        replay_failures.append(f"block {number}: {replay.failure}")
            continue

        block_count += 1
        block_run = run_example_block(session, commands)
        if block_run.failure:
            line_no = text.count("\n", 0, m.start()) + 1
            raise ExampleRunError(f"shell block {number} (line {line_no}, first command "
                                  f"`{commands[0]}`): {block_run.failure}")
        rebuilt: list[str] = []
        i = 0
        k = 0
        while i < len(lines):
            line = lines[i]
            if not line.startswith(PROMPT):
                # Lines before the first dragonfly> get passed through
                # (e.g. comments at the start of a block).
                rebuilt.append(line)
                i += 1
                continue
            output = block_run.outputs[k]
            actual = output.split("\n") if output else []
            rebuilt.append(line)
            rebuilt.extend(actual)
            reply = error_reply(output)
            if reply:
                errors.append({"block": number, "command": commands[k], "reply": reply})
            k += 1
            invocation_count += 1
            # Skip the LLM's predicted output — keep walking until next
            # `dragonfly>` line or end of block — but keep the blank and
            # comment lines that end it.
            j = i + 1
            while j < len(lines) and not lines[j].startswith(PROMPT):
                j += 1
            rebuilt.extend(kept_separator_lines(lines[i + 1:j], actual))
            i = j
        out_parts.append("```shell\n" + "\n".join(rebuilt) + "\n```")

    out_parts.append(text[last_pos:])
    new_text = "".join(out_parts)

    if invocation_count:
        notes.append(
            f"verified {invocation_count} `dragonfly>` invocation(s) in "
            f"{block_count} block(s), one redis-cli session per block (FLUSHALL first)"
            + (f"; {len(errors)} error repl(ies)" if errors else "")
        )
    if replayed:
        notes.append(
            f"replayed {replayed} unchanged block(s) before the changed ones, in page "
            "order, for the server state they leave (ACL users, CONFIG, scripts); "
            "their text is kept"
        )
    if replay_failures:
        notes.append("replayed unchanged block(s) that did not complete (their text is "
                     "kept): " + "; ".join(replay_failures))
    if kept["topology"]:
        notes.append(
            f"preserved {kept['topology']} topology-dependent shell block(s) "
            "without standalone output substitution"
        )
    if kept["push-mode"]:
        notes.append(
            f"preserved {kept['push-mode']} push-mode shell block(s) (SUBSCRIBE, "
            "PSUBSCRIBE, SSUBSCRIBE or MONITOR never return in a redis-cli session); "
            "their output is as written"
        )
    if new_kept:
        notes.append(
            f"{len(new_kept)} of the topology-dependent or push-mode block(s) are not in "
            f"the input page (block(s) {', '.join(map(str, new_kept))}): they were not "
            "run, so their output is the LLM's prediction"
        )
    if unchanged_block_count:
        notes.append(
            f"preserved {unchanged_block_count} unchanged shell block(s) "
            "without dynamic-output churn"
        )
    return new_text, errors, notes


# --- Sibling style reference ------------------------------------------------

_EXCLUDE_SIBLING_NAMES = frozenset({
    "index.md", "_category_.md", "README.md",
})


def pick_sibling_style_reference(file_rel: str) -> tuple[str, str] | None:
    """Pick a sibling page in the same directory to act as a visual style
    template. We prefer the shortest sibling that has H2 sections — short
    pages are cleaner templates and less likely to drown the prompt.
    Returns (relative_path, full_text) or None if no sibling fits."""
    target = (REPO_ROOT / file_rel).resolve()
    parent = target.parent
    candidates: list[tuple[int, Path, str]] = []
    for f in parent.glob("*.md"):
        if f == target or f.name in _EXCLUDE_SIBLING_NAMES:
            continue
        try:
            text = f.read_text(encoding="utf-8")
        except OSError:
            continue
        if len(text) < 200:
            continue
        if "\n## " not in text:
            continue
        candidates.append((len(text), f, text))
    if not candidates:
        return None
    candidates.sort()
    _, path, text = candidates[0]
    if len(text) > 4000:
        text = text[:4000] + "\n\n<!-- (sibling truncated for brevity) -->\n"
    return str(path.relative_to(REPO_ROOT)), text


# --- Phase 2: Update each file ----------------------------------------------

UPDATE_SYSTEM = """\
You are updating a single Dragonfly DB documentation page so that it matches
the current state of the source code. Strict rules — violations make the
page unusable:

1. Only assert facts that are supported by the inputs you receive (the
   current page, the source code excerpts, the Docker-verified examples,
   the runtime facts, and the diff_context if provided). Never invent
   options, return shapes, behaviors, complexities, or anything else.
2. For complexity, give the GENERAL CASE only. Do not list edge cases.
   If you cannot derive a clear general-case complexity from the source,
   state the complexity in plain words instead of inventing a Big-O.
3. Every example shown as a `dragonfly>` interaction inside a ```shell```
   block (existing or new) is normally verified in Docker by the caller AFTER
   you produce the markdown. The caller replaces the lines following each
   eligible `dragonfly>` line with the actual server output.

   Commands whose output depends on replication, failover, native-cluster
   configuration, or another remote node are intentionally NOT executed in the
   standalone verification container. Neither are blocks with SUBSCRIBE,
   PSUBSCRIBE, SSUBSCRIBE or MONITOR: they never return in a redis-cli
   session. Their input records have `skipped: true`. Preserve such existing
   blocks byte-for-byte: command lines, output, comments, and explanatory
   prose. A response from an unconfigured or emulated standalone instance is
   never evidence that a curated replica or cluster example is wrong.

   Output order for map-like or shard-aggregated replies can be nondeterministic.
   Do not rewrite an existing example merely to match a different valid ordering
   or another run's dynamic values.

   The caller runs each ```shell``` block in ONE redis-cli session that
   starts with `FLUSHALL`, so each block starts from a clean keyspace —
   prior examples never leak into the next one. Within a block the
   connection persists: keys, SELECT, AUTH, HELLO 3, MULTI/EXEC and CLIENT
   settings carry from one `dragonfly>` line to the next, so `SET k 1`
   followed by `GET k` works as a chain. Keys and connection state do not
   carry into the next block. Server state that FLUSHALL keeps (ACL users,
   CONFIG SET values, loaded scripts) does, in page order, as for a reader
   who runs the blocks one after another: a block that re-creates an ACL
   user an earlier block made modifies that user.

   In docker_example_observations, `error_reply: true` marks a server error
   reply. The caller writes such replies into the page as the example
   output, so a block should only produce an error where the page means to
   show one. Records with `not_run: true` and a `failure` are commands the
   caller could not complete or trust (no reply within 30 s, a reply
   redis-cli cannot parse, a lost connection, or a FLUSHALL the server
   refused); they say nothing about server behavior. A changed or new
   block that does not complete makes the caller reject the whole page, so
   never write a blocking command (BLPOP, BRPOP, BLMOVE, XREAD BLOCK, ...
   with timeout 0) that waits for data no earlier line of the same block
   provides, a command that closes the block's own connection (QUIT, or
   CLIENT KILL matching it), or a command that makes the server refuse the
   next block's FLUSHALL (requirepass, or turning the default user off).

   Rules:
     * Place new examples in their natural place — inside the page's
       existing `## Examples` (or equivalent) section, beside related
       existing examples. NEVER append a new fenced block at the bottom
       of the page just to host a new example — that changes the page
       structure.
     * Each block should be SELF-CONTAINED. If demonstrating a command
       requires keys / streams / sets to already exist, include the
       setup commands at the top of the same block (e.g. write
       `dragonfly> RPUSH mylist a b c` before `dragonfly> LRANGE mylist 0 -1`).
       Extending an example with a few setup lines so the reader sees a
       meaningful result is encouraged.
     * For existing examples, you may keep them as-is or extend them
       with setup lines to make them clearer. The caller re-verifies
       every eligible invocation either way.
     * Do not invent commands you cannot justify from the source or
       runtime facts.
4. **Do NOT modify, remove or add a `**ACL categor(y|ies):**` line**,
   including qualified variants such as
   `**ACL categories (Dragonfly v2.0.2):**`. That metadata is owned by a
   separate tool (`acl_sync.py`). Leave every such line byte-identical to
   what is in the input page — same prefix (with or without leading dash),
   same label, same category list, same order — and do not add one to a
   page that has none.
5. **Do NOT change the page structure.** Keep every existing section in
   its current position. Do not add new top-level (`##`) sections that
   the input page does not already have. Do not move examples or any
   content between sections. Do not split or merge sections. Change
   CONTENT inside existing sections only.
6. Preserve the page's frontmatter, `import PageTitle from ...` line,
   and the `<PageTitle ...>` tag verbatim — they are required by the
   site build.
7. Preserve any human-written context that the source/Docker cannot
   refute. If you cannot verify a claim and cannot disprove it, leave it
   unchanged.
8. Match the **existing visual style** of the page EXACTLY. The reader
   must not be able to tell the page was edited just by looking at the
   formatting. Specifically, do NOT change:
     * heading levels or section hierarchy
     * whether the metadata block uses bullets (`- **Time complexity:**`)
       or plain (`**Time complexity:**`)
     * how parameters are introduced (plain bullets vs
       `<details><summary>` blocks)
     * how examples are framed (with/without intro paragraph,
       single-block vs per-step)
     * link style (relative vs absolute, with/without titles)
     * paragraph break conventions, list bullet character
   You will receive a `sibling_style_reference` — another page from the
   same category — purely as a style template. Match its conventions
   when the input page has gaps. Never introduce a new style that
   would make this page look different from its siblings. Change
   CONTENT, not FORM.
9. Cross-page link lists must already be at the END of the page if the
   input has them. Do not move existing inline links into a list at the
   end. Do not introduce a new "See also" section if the input does not
   have one.
10. Never write a bare `<placeholder>` token (e.g. `<key>`, `<pattern>`,
    `<sha1>`) outside a fenced ``` ... ``` code block. Docusaurus parses
    prose as MDX 3 and treats `<key>` as an unclosed JSX tag — the build
    WILL fail. In prose, use inline code (`` `<key>` ``) or plain words
    ("the key"). Standard HTML elements like `<details>`, `<summary>`,
    `<code>`, `<b>` ARE allowed in prose because MDX recognizes them.
11. If the source code, runtime facts, and Docker-verified examples all
    confirm what the page already says, output the markdown BYTE-IDENTICAL
    to the input. Do not rewrite for style; do not paraphrase; do not
    add or remove blank lines that were already there. The caller skips
    the disk write when the output equals the input — saving a no-op
    edit. If you say in your `notes` that the output is byte-identical
    to the input, then the markdown field MUST actually be byte-identical
    — it is checked.
12. NEVER reply with a placeholder like `...`, `TBD`, "see input", or
    "unchanged from above" inside the `markdown` field. The `markdown`
    field MUST contain the FULL page content, every line. The caller
    rejects any output that is shorter than half of the input or that
    is just an ellipsis — and treats that as a hard failure that
    prevents the file from being written.

If `diff_context` is present in your input it tells you which source
commits motivated this update — focus the edit on what those commits
changed. If `diff_context` is absent (e.g. this file came from a manual
override), perform a full review against the current source state
without assuming which areas need attention.

Output JSON only. The first character must be `{` and the last must be `}`.
No preamble, no markdown fences around the JSON, no explanation.

Schema:

  { "markdown": "<full updated page content>",
    "notes":    ["<short bullet about a decision>", ...] }

The caller verifies every eligible `dragonfly>` invocation in your `markdown`
by running it in a Docker container and substituting the captured output.
Topology-dependent and push-mode blocks are preserved instead. You do not
have to predict eligible server output — but you DO have to put each example
in the correct section (no appending blocks just to host examples).
"""

UPDATE_SCHEMA = strict_object_schema({
    "markdown": {"type": "string"},
    "notes": {"type": "array", "items": {"type": "string"}},
})


def build_update_user_text(
    file_rel: str,
    page_text: str,
    handler_info: dict | None,
    facts_entry: dict | None,
    acl_categories: list[str],
    docker_examples: list[dict],
    sibling_style: tuple[str, str] | None = None,
    diff_context: dict | None = None,
) -> str:
    parts = [
        f"=== file_path ===\n{file_rel}",
        "",
        "=== current_page ===",
        page_text,
        "",
    ]
    if diff_context is not None:
        parts += [
            "=== diff_context (commits between the two tags that motivated "
            "this update — focus your edit on what they changed) ===",
            json.dumps(diff_context, indent=2, ensure_ascii=False),
            "",
        ]
    else:
        parts += [
            "=== diff_context ===",
            "(absent — this file came from a manual override; review the "
            "current source state generally without assuming a focus area)",
            "",
        ]
    if sibling_style is not None:
        sib_path, sib_text = sibling_style
        parts += [
            "=== sibling_style_reference (do NOT copy content; only mirror "
            "formatting / structure conventions) ===",
            f"path: {sib_path}",
            sib_text,
            "",
        ]
    if handler_info:
        parts += [
            "=== source_handler (current state at the new tag) ===",
            f"file: {handler_info['file']}",
            f"registration_line: {handler_info['registration_line']}",
            f"function: {handler_info['handler_function']}",
            "body:",
            handler_info["handler_body"],
            "",
        ]
    if facts_entry:
        parts += [
            "=== runtime_facts (COMMAND output) ===",
            json.dumps(facts_entry, indent=2),
            "",
        ]
    if acl_categories:
        parts += [
            "=== acl_categories (informational only — DO NOT modify the "
            "ACL line in the page; this is owned by acl_sync.py) ===",
            ", ".join(sorted(acl_categories)),
            "",
        ]
    parts += [
        "=== docker_example_observations (one redis-cli session per ```shell block, "
        "FLUSHALL first; topology-dependent and push-mode blocks are skipped) ===",
        json.dumps(docker_examples, indent=2, ensure_ascii=False),
        "",
        "=== task ===",
        "Produce the JSON {markdown, notes}. JSON only.",
    ]
    return "\n".join(parts)


def needs_emulated_cluster(handler_info: dict | None, command: str | None) -> bool:
    if command and command.split()[0] in {"CLUSTER", "READONLY", "READWRITE",
                                           "DFLYCLUSTER"}:
        return True
    if handler_info and "cluster_family.cc" in handler_info.get("file", ""):
        return True
    return False


def page_acl_categories(rel: str, command: str | None, facts: dict) -> list[str]:
    """ACL categories the server checks for the command a command-reference
    page documents, resolved the way acl_sync.py does (acl_model.resolve): the
    command's own entry, an ACL-only subcommand entry such as `CLIENT|KILL`,
    or the container's entry. Pages outside docs/command-reference/ get none:
    an H1 such as "Cluster Mode" would resolve to CLUSTER's categories."""
    if not command or not rel.startswith("docs/command-reference/"):
        return []
    resolution = acl_model.resolve(command, acl_model.command_acl_view(facts),
                                   acl_model.server_commands(facts))
    return resolution.categories or []


def save_debug_markdown(kind: str, rel: str, markdown: str) -> str:
    """Save LLM markdown that was not written to the page; returns its path."""
    LLM_DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    slug = re.sub(r"[^a-z0-9]+", "_", rel.lower())[:60]
    debug = LLM_DEBUG_DIR / f"{kind}_{slug}_{ts}.md"
    debug.write_text(markdown, encoding="utf-8")
    try:
        return str(debug.relative_to(REPO_ROOT))
    except ValueError:
        return str(debug)


def update_one_file(
    entry: dict,
    after_tag: str,
    facts: dict,
    src: Path,
    dry_run: bool,
) -> dict:
    """Update one file. Returns a result record."""
    result: dict = {
        "path": entry.get("path"),
        "status": "pending",
        "reason_input": entry.get("reason", ""),
        "notes": [],
    }
    try:
        rel = normalize_doc_path(entry.get("path"))
    except ValueError as e:
        result["status"] = "failed"
        result["error"] = str(e)
        return result
    result["path"] = rel
    abs_path = REPO_ROOT / rel
    if rel in OWNED_PAGES:
        result["status"] = "skipped"
        result["error"] = f"owned by {OWNED_PAGES[rel]}; docs_sync does not edit it"
        return result
    if not abs_path.exists():
        result["status"] = "missing"
        result["error"] = f"file not found: {rel}"
        return result
    if dry_run:
        result["status"] = "skipped"
        result["notes"].append("dry-run: not sent to OpenAI, not written")
        return result

    page_text = abs_path.read_text(encoding="utf-8")
    h1 = extract_h1(page_text)
    command = h1.upper() if h1 else None
    facts_entry = facts.get("data", {}).get("commands", {}).get(command)
    acl_cats = page_acl_categories(rel, command, facts)
    handler_info = (find_command_handler_source(src, command) if command else None)

    invocations = extract_redis_invocations(page_text)
    docker_examples: list[dict] = []
    session = None
    client = None
    is_command_page = bool(facts_entry)
    needs_docker = bool(invocations) or is_command_page
    emu = needs_emulated_cluster(handler_info, command)
    observed = False

    try:
        if needs_docker:
            try:
                session = boot_docker(after_tag, emulated_cluster=emu)
            except Exception as e:
                # Without a server the LLM's predicted example output would be
                # written unverified, so do not update the page at all.
                result["status"] = "failed"
                result["error"] = f"docker boot failed: {error_detail(e)}"
                return result
        if session and invocations:
            observed = True
            try:
                docker_examples, observe_notes = observe_examples(session, page_text)
            except DockerTimeout as e:
                result["status"] = "failed"
                result["error"] = (f"running the page's current examples failed: {e}; "
                                   "the page was not sent to OpenAI")
                return result
            result["notes"].extend(observe_notes)

        if not os.getenv("OPENAI_API_KEY"):
            result["status"] = "skipped"
            result["error"] = "OPENAI_API_KEY not set"
            return result
        try:
            client = create_client()
        except RuntimeError as exc:
            result["status"] = "skipped"
            result["error"] = str(exc)
            return result
        sibling_style = pick_sibling_style_reference(rel)
        if sibling_style:
            result["notes"].append(
                f"using sibling style reference: {sibling_style[0]}"
            )
        diff_context = entry.get("diff_context")
        if diff_context:
            result["notes"].append(
                f"using diff_context ({len(diff_context.get('commits_per_file', []))} "
                f"related source file(s))"
            )
        user_text = build_update_user_text(
            rel, page_text, handler_info, facts_entry, acl_cats,
            docker_examples, sibling_style, diff_context,
        )
        print(f"  -> {rel}: calling OpenAI ({UPDATE_MODEL})...")
        parsed, usage = call_llm_streaming(
            client, UPDATE_SYSTEM, user_text, UPDATE_MAX_TOKENS,
            UPDATE_MODEL, "docs_update", UPDATE_SCHEMA,
        )
        print(f"     tokens: in={usage['input_tokens']} "
              f"out={usage['output_tokens']} "
              f"reasoning={usage['reasoning_tokens']}")
        new_md = parsed.get("markdown", "")
        notes = parsed.get("notes", []) or []
        result["notes"].extend(notes)

        if not new_md.strip():
            result["status"] = "failed"
            result["error"] = "LLM returned empty markdown"
            return result

        # Structural validation — catches catastrophic LLM failures like
        # returning `...`, truncating mid-document, or losing required
        # structure. Run BEFORE Docker verification because we don't want
        # to spend Docker time on garbage output.
        struct_errors = validate_update_output(page_text, new_md)
        if struct_errors:
            debug = save_debug_markdown("docs_sync_rejected", rel, new_md)
            result["status"] = "failed"
            result["error"] = (
                f"structural validation failed: {struct_errors}; "
                f"raw LLM markdown saved to {debug}"
            )
            return result

        # Verify changed and new eligible examples in the LLM's markdown by
        # running them in Docker and substituting the actual output. Unchanged,
        # topology-dependent and push-mode blocks are preserved to avoid false
        # churn. A block that does not complete leaves its output unknown, so
        # the page is not written (as for a container that does not boot).
        unverified = unverified_new_blocks(new_md, page_text)
        if unverified:
            result["unverified_blocks"] = unverified
        if (session is None or observed) and any(
                kind == "changed" for _n, _m, kind in classify_blocks(new_md, page_text)):
            # The pre-LLM pass ran every current example on this server, and
            # FLUSHALL keeps what they left (ACL users, CONFIG SET, scripts):
            # a changed block would see state from examples after it. Verify
            # on a fresh server; earlier blocks are replayed in page order. A
            # page that had no examples and no container gets one here, so
            # examples the LLM added are verified too.
            if session:
                kill_docker(session)
                session = None
            try:
                session = boot_docker(after_tag, emulated_cluster=emu)
            except Exception as e:
                debug = save_debug_markdown("docs_sync_unverified", rel, new_md)
                result["status"] = "failed"
                result["error"] = (f"docker boot for example verification failed: "
                                   f"{error_detail(e)}; the page was not written; raw LLM "
                                   f"markdown saved to {debug}")
                return result
        if session:
            try:
                new_md, exec_errors, exec_notes = verify_and_substitute_examples(
                    new_md, session, baseline_text=page_text,
                )
            except (ExampleRunError, DockerTimeout) as e:
                debug = save_debug_markdown("docs_sync_unverified", rel, new_md)
                result["status"] = "failed"
                result["error"] = (f"example verification failed: {e}; the page was not "
                                   f"written; raw LLM markdown saved to {debug}")
                result["notes"].append(f"example block did not complete: {e}")
                return result
            result["notes"].extend(exec_notes)
            if exec_errors:
                result["example_errors"] = exec_errors
                result["notes"].append(
                    f"{len(exec_errors)} example repl(ies) are errors and were written "
                    f"into the page as the example output: "
                    + "; ".join(f"block {e['block']}: {e['command']} -> {e['reply']}"
                                for e in exec_errors[:5])
                    + ("; ..." if len(exec_errors) > 5 else "")
                )

        # MDX safety: wrap bare `<placeholder>` tokens, convert indented
        # code-with-placeholders to fenced text blocks.
        safe_md = fix_mdx_jsx_unsafe(new_md)
        if safe_md != new_md:
            result["notes"].append(
                "applied MDX safety pass (wrapped placeholders / "
                "fenced indented blocks)"
            )
            new_md = safe_md

        gone = removed_prose(page_text, new_md)
        if gone:
            result["removed_text"] = gone
            result["notes"].append(f"{len(gone)} line(s) of existing prose were removed or "
                                   f"rewritten; check each against the source")

        # No-change-skip: if the final markdown equals the input — exactly
        # or after stripping cosmetic-only differences (trailing spaces,
        # collapsed blank-line runs) — the page already matches reality.
        # Do not write a no-op edit, the git diff would be pure noise.
        if new_md == page_text:
            result["status"] = "unchanged"
            result["notes"].append(
                "page already matches source/Docker — no write performed"
            )
            return result
        if normalize_for_compare(new_md) == normalize_for_compare(page_text):
            result["status"] = "unchanged"
            result["notes"].append(
                "page differs from input only in whitespace — no write performed"
            )
            return result

        abs_path.write_text(new_md, encoding="utf-8")
        result["status"] = "updated"
    finally:
        if client:
            client.close()
        if session:
            kill_docker(session)
    return result


def update_phase(plan: dict, after_tag: str, skip_pull: bool, dry_run: bool,
                 filter_glob: str = "") -> list[dict]:
    print(f"\n[Phase 2] Update {len(plan['files_to_update'])} file(s) "
          f"against tag {after_tag}")
    source_commit = ensure_dragonfly_checkout(after_tag)
    src = DRAGONFLY_CHECKOUT
    planned = plan.get("after_commit")
    if planned is None:
        print("  WARNING: plan records no after_commit (made before commit tracking); "
              f"cannot verify it was discovered at {after_tag}'s current commit",
              file=sys.stderr)
    elif planned != source_commit:
        raise RuntimeError(
            f"plan was discovered at {after_tag} @ {dfly_refs.short(planned)}, but "
            f"{after_tag} is now {dfly_refs.short(source_commit)}; the tag moved, "
            f"so re-run discover"
        )
    if plan.get("before_commit") and plan.get("before"):
        before_now = resolve_before(plan["before"])
        if before_now != plan["before_commit"]:
            raise RuntimeError(
                f"plan was discovered from {plan['before']} @ "
                f"{dfly_refs.short(plan['before_commit'])}, but {plan['before']} is now "
                f"{dfly_refs.short(before_now)}; the tag moved, so re-run discover"
            )

    # Source, image and facts must all come from the tag's current commit.
    image_ref = f"{DRAGONFLY_IMAGE}:{after_tag}"
    if not skip_pull:
        dfly_refs.docker_pull(image_ref)
    version, image_commit = dfly_refs.image_version(image_ref)
    print(f"  image: {version}")
    if not image_commit:
        raise RuntimeError(f"`dragonfly --version` in {image_ref} has no build commit SHA "
                           f"({version}); cannot verify it is {after_tag}")
    facts = dfly_refs.load_facts(after_tag, FACTS_DIR, image_ref,
                                 skip_pull=True, refresh=False)
    dfly_refs.check_same_commit(after_tag, source=source_commit, image=image_commit,
                                facts=dfly_refs.facts_commit(facts))
    try:
        acl_model.command_acl_view(facts)  # pages read their ACL categories from it
    except acl_model.FactsError as e:
        raise RuntimeError(f"facts for {after_tag}: {e}") from None

    results: list[dict] = []
    entries = []
    for e in plan["files_to_update"]:
        try:
            e = {**e, "path": normalize_doc_path(e.get("path"))}
        except ValueError:
            entries.append(e)  # invalid path: update_one_file reports it as failed
            continue
        if matches_filter(e["path"], filter_glob):
            entries.append(e)
    for entry in entries:
        try:
            results.append(update_one_file(
                entry, after_tag, facts, src, dry_run,
            ))
        except Exception as e:
            results.append({
                "path": entry["path"],
                "status": "error",
                "error": str(e),
                "notes": [],
            })
    return results


# --- Main --------------------------------------------------------------------

def error_detail(e: Exception) -> str:
    if isinstance(e, subprocess.CalledProcessError):
        return f"{' '.join(e.cmd)} failed: {(e.stderr or '').strip()}"
    return str(e)


def parse_also_update(path: Path | None) -> list[str]:
    if not path:
        return []
    out: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--before", help="Older Dragonfly tag.")
    ap.add_argument("--after", help="Newer Dragonfly tag.")
    ap.add_argument("--also-update", type=Path,
                    help="Text file with paths to force-include in the plan, "
                         "one per line.")
    ap.add_argument("--filter", default="",
                    help="Glob to limit which md files are processed "
                         "(docs/command-reference/strings/* or command-reference/strings/*).")
    ap.add_argument("--discover-only", action="store_true",
                    help="Run Phase 1 only; print the plan and exit.")
    ap.add_argument("--update-only-from", type=Path,
                    help="Skip Phase 1; load this saved plan JSON and run "
                         "Phase 2 against it.")
    ap.add_argument("--skip-pull", action="store_true",
                    help="Skip docker pull for the Dragonfly image.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Run the checks (tags, image, facts) and list the pages without "
                         "calling OpenAI or writing pages, plans or results. The checks may "
                         "still check out the source, pull the image and capture facts.")
    args = ap.parse_args()

    if args.update_only_from:
        plan = json.loads(args.update_only_from.read_text(encoding="utf-8"))
        plan["_plan_path"] = str(args.update_only_from.resolve()
                                 .relative_to(REPO_ROOT))
        after_tag = plan.get("after") or args.after
        if not after_tag:
            ap.error("--update-only-from plan has no `after` tag and "
                     "--after not given")
    else:
        if not args.before or not args.after:
            ap.error("--before and --after are required (unless "
                     "--update-only-from is used)")
        also = parse_also_update(args.also_update)
        try:
            plan = discover_phase(args.before, args.after, also, args.filter, args.dry_run)
        except (RuntimeError, subprocess.CalledProcessError) as e:
            print(f"ERROR: {error_detail(e)}", file=sys.stderr)
            return 2
        if args.discover_only:
            print("\n--- Plan summary ---")
            for entry in plan["files_to_update"]:
                print(f"  {entry['path']}")
                print(f"    reason: {entry.get('reason', '')}")
            return 0
        after_tag = args.after

    try:
        results = update_phase(plan, after_tag, args.skip_pull, args.dry_run,
                               args.filter)
    except (RuntimeError, subprocess.CalledProcessError) as e:
        print(f"ERROR: {error_detail(e)}", file=sys.stderr)
        return 2

    counters = {"updated": 0, "unchanged": 0, "failed": 0, "skipped": 0,
                "missing": 0, "error": 0}
    for r in results:
        counters[r["status"]] = counters.get(r["status"], 0) + 1
    print(f"\n--- Phase 2 summary ---")
    for k, v in counters.items():
        if v:
            print(f"  {k}: {v}")
    if counters.get("failed") or counters.get("error"):
        print("\nFailures:")
        for r in results:
            if r["status"] in ("failed", "error"):
                print(f"  {r['path']}: {r.get('error', '?')}")
    flagged = [(r, e) for r in results for e in r.get("example_errors", [])]
    if flagged:
        print(f"\nError replies in verified examples ({len(flagged)}); the page shows "
              "them as the output. Keep the documented error cases, fix the rest:")
        for r, e in flagged:
            print(f"  {r['path']} ({r['status']}): block {e['block']}: "
                  f"{e['command']} -> {e['reply']}")
    rewritten = [r for r in results if r.get("removed_text") and r["status"] == "updated"]
    if rewritten:
        print(f"\nExisting prose removed or rewritten on {len(rewritten)} page(s); check that "
              "each line was wrong before keeping the change:")
        for r in rewritten:
            print(f"  {r['path']}: {len(r['removed_text'])} line(s)")
            for line in r["removed_text"][:3]:
                print(f"      - {line[:140]}")
            if len(r["removed_text"]) > 3:
                print(f"      ... see removed_text in the results file")
    unverified = [(r, b) for r in results for b in r.get("unverified_blocks", [])]
    if unverified:
        print(f"\nNew example blocks that were not run ({len(unverified)}); their output "
              "is the LLM's prediction. Check them by hand:")
        for r, b in unverified:
            print(f"  {r['path']} ({r['status']}): block {b['block']} ({b['kind']}): "
                  f"{b['command']}")

    if args.dry_run:
        print("\nPages:")
        for r in results:
            print(f"  {r['status']}: {r['path']}" + (f" — {r['error']}" if r.get("error") else ""))
        print("\n(dry-run — results not saved)")
        return 0 if not (counters.get("failed") or counters.get("error")) else 1
    PLANS_DIR.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    results_path = PLANS_DIR / f"results_{ts}.json"
    results_path.write_text(
        json.dumps({
            "plan_path": plan.get("_plan_path"),
            "after": after_tag,
            "results": results,
        }, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"\nResults saved: {results_path.relative_to(REPO_ROOT)}")
    return 0 if not (counters.get("failed") or counters.get("error")) else 1


if __name__ == "__main__":
    sys.exit(main())
