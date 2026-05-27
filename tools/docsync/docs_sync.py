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
  * Boot a Dragonfly Docker container at <after>. Run every redis-cli
    invocation already on the page and capture the actual output. New
    examples the LLM proposes are also run in Docker before they're
    accepted; if a proposed example errors out it is dropped.
  * The LLM produces the updated markdown with strict rules: only facts
    that the source or Docker confirms; general-case complexity only;
    never invent options or behaviors.

CLI:
    python docs_sync.py --before v1.37.0 --after v1.38.0
    python docs_sync.py --before v1.37.0 --after v1.38.0 --also-update extra.txt
    python docs_sync.py --before v1.37.0 --after v1.38.0 --discover-only
    python docs_sync.py --update-only-from tools/generated/update_plans/<ts>.json
    python docs_sync.py --before v1.37.0 --after v1.38.0 --dry-run
    python docs_sync.py --before v1.37.0 --after v1.38.0 --filter "command-reference/strings/*"
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = REPO_ROOT / "docs"
GENERATED = REPO_ROOT / "tools" / "generated"
PLANS_DIR = GENERATED / "update_plans"
LLM_DEBUG_DIR = GENERATED / "llm_debug"
FACTS_DIR = GENERATED / "facts"
DFLY_FACTS = REPO_ROOT / "tools" / "docsync" / "dfly_facts.py"

DRAGONFLY_REPO_URL = "https://github.com/dragonflydb/dragonfly.git"
DRAGONFLY_CHECKOUT = Path("/tmp/dragonfly-docsync")
DRAGONFLY_IMAGE = "docker.dragonflydb.io/dragonflydb/dragonfly"

MODEL = "claude-sonnet-4-6"
DISCOVER_MAX_TOKENS = 16000
UPDATE_MAX_TOKENS = 24000
PING_TIMEOUT_S = 30


# --- Helpers ----------------------------------------------------------------

def run(cmd: list[str], cwd: Path | None = None,
        check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def ensure_dragonfly_checkout(tag: str, refresh: bool = False) -> Path:
    if not (DRAGONFLY_CHECKOUT / ".git").exists():
        DRAGONFLY_CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        print(f"  cloning Dragonfly source to {DRAGONFLY_CHECKOUT}...")
        run(["git", "clone", "--quiet", DRAGONFLY_REPO_URL, str(DRAGONFLY_CHECKOUT)])
    if refresh:
        run(["git", "fetch", "--tags", "--quiet"], cwd=DRAGONFLY_CHECKOUT, check=False)
    run(["git", "checkout", "--quiet", tag], cwd=DRAGONFLY_CHECKOUT, check=False)
    return DRAGONFLY_CHECKOUT


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


def collect_md_index(filter_glob: str = "") -> list[dict]:
    out: list[dict] = []
    for f in sorted(DOCS_DIR.rglob("*.md")):
        rel = str(f.relative_to(REPO_ROOT))
        if filter_glob and not fnmatch(rel, filter_glob) \
                and not fnmatch(str(f.relative_to(DOCS_DIR)), filter_glob):
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
    src = ensure_dragonfly_checkout(after)
    # Make sure we have <before> too — fetch all tags.
    run(["git", "fetch", "--tags", "--quiet"], cwd=src, check=False)
    log = run(["git", "log", "--no-merges", "--pretty=%h %s",
               f"{before}..{after}"], cwd=src, check=False).stdout
    stat = run(["git", "diff", "--stat", f"{before}..{after}"],
               cwd=src, check=False).stdout
    name_only = run(["git", "diff", "--name-only", f"{before}..{after}"],
                    cwd=src, check=False).stdout
    return {
        "before": before,
        "after": after,
        "commits": [l for l in log.splitlines() if l.strip()],
        "stat": stat,
        "files_changed": [l for l in name_only.splitlines() if l.strip()],
    }


def commits_touching_file(before: str, after: str, src_file: str) -> list[str]:
    """Return commits between before and after that touched src_file."""
    p = run(
        ["git", "log", "--no-merges", "--pretty=%h %s",
         f"{before}..{after}", "--", src_file],
        cwd=DRAGONFLY_CHECKOUT, check=False,
    )
    return [l for l in p.stdout.splitlines() if l.strip()]


def build_diff_context(before: str, after: str, related_files: list[str],
                       reason: str) -> dict:
    """Compose the per-file diff_context to pass to the update LLM session."""
    commits_per_file = []
    for f in related_files:
        commits = commits_touching_file(before, after, f)
        if commits:
            commits_per_file.append({"file": f, "commits": commits})
    return {
        "before": before,
        "after": after,
        "discovery_reason": reason,
        "commits_per_file": commits_per_file,
    }


# --- LLM helpers -------------------------------------------------------------

def _extract_json_object(text: str) -> dict | None:
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    fence = re.search(r"```(?:json|JSON)?\s*\n(.*?)\n```", text, re.DOTALL)
    if fence:
        try:
            return json.loads(fence.group(1).strip())
        except json.JSONDecodeError:
            pass
    depth = 0
    in_str: str | None = None
    start = -1
    i = 0
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
        elif c == "{":
            if depth == 0:
                start = i
            depth += 1
        elif c == "}":
            depth -= 1
            if depth == 0 and start != -1:
                try:
                    return json.loads(text[start:i + 1])
                except json.JSONDecodeError:
                    start = -1
        i += 1
    return None


def call_llm_streaming(client, system_prompt: str, user_text: str,
                       max_tokens: int, label: str) -> tuple[dict, dict]:
    text_parts: list[str] = []
    chars = 0
    print(f"  streaming response", end="", flush=True)
    with client.messages.stream(
        model=MODEL,
        max_tokens=max_tokens,
        system=[{"type": "text", "text": system_prompt,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_text}],
    ) as stream:
        for chunk in stream.text_stream:
            text_parts.append(chunk)
            chars += len(chunk)
            if chars % 4000 < len(chunk):
                print(".", end="", flush=True)
        response = stream.get_final_message()
    print(f" done ({chars} chars)")
    text = "".join(text_parts).strip()
    parsed = _extract_json_object(text)
    if parsed is None:
        LLM_DEBUG_DIR.mkdir(parents=True, exist_ok=True)
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        debug = LLM_DEBUG_DIR / f"docs_sync_{label}_{ts}.txt"
        debug.write_text(text, encoding="utf-8")
        raise RuntimeError(
            f"LLM response did not contain a parseable JSON object; "
            f"raw saved to {debug.relative_to(REPO_ROOT)}"
        )
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }
    return parsed, usage


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


def build_discover_prompt(diff: dict, md_index: list[dict]) -> str:
    parts = [
        f"=== source diff summary {diff['before']}..{diff['after']} ===",
        f"commits ({len(diff['commits'])}):",
        "\n".join(diff["commits"][:300]),
        ("..." if len(diff["commits"]) > 300 else ""),
        "",
        "files_changed (top of diff --stat):",
        "\n".join(diff["stat"].splitlines()[:200]),
        ("..." if len(diff["stat"].splitlines()) > 200 else ""),
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
                   md_filter: str) -> dict:
    print(f"\n[Phase 1] Discover updates needed between {before} and {after}")
    diff = collect_source_diff_summary(before, after)
    print(f"  source diff: {len(diff['commits'])} commits, "
          f"{len(diff['files_changed'])} files changed")
    md_index = collect_md_index(md_filter)
    print(f"  docs index:  {len(md_index)} markdown file(s)")

    plan: dict = {
        "before": before,
        "after": after,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files_to_update": [],
        "llm_summary": "",
        "manual_overrides": [],
    }

    if not os.getenv("ANTHROPIC_API_KEY"):
        print("  WARNING: ANTHROPIC_API_KEY not set — skipping LLM analysis. "
              "Plan will only contain --also-update entries (if any).")
    else:
        try:
            import anthropic
        except ImportError:
            print("  WARNING: anthropic SDK missing — LLM analysis skipped.")
        else:
            client = anthropic.Anthropic()
            user_text = build_discover_prompt(diff, md_index)
            print("  asking Claude to triage...")
            parsed, usage = call_llm_streaming(
                client, DISCOVER_SYSTEM, user_text,
                DISCOVER_MAX_TOKENS, "discover",
            )
            print(f"  tokens: in={usage['input_tokens']} "
                  f"out={usage['output_tokens']}")
            plan["files_to_update"] = parsed.get("files_to_update", []) or []
            plan["llm_summary"] = parsed.get("no_update_needed_summary", "") or ""

    # Attach diff_context for every LLM-discovered entry. Files added via
    # --also-update get diff_context = null so the update session does NOT
    # narrow its focus based on the source diff.
    for entry in plan["files_to_update"]:
        related = entry.get("related_source_files", []) or []
        reason = entry.get("reason", "")
        entry["diff_context"] = build_diff_context(before, after, related, reason)

    if also_update:
        existing_paths = {e["path"] for e in plan["files_to_update"]}
        for path in also_update:
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
    r"^```shell[ \t]*\n(?P<body>.*?)^```\s*$",
    re.DOTALL | re.MULTILINE,
)


def extract_redis_invocations(text: str) -> list[str]:
    """Return every `dragonfly>` line found inside ```shell blocks."""
    invocations: list[str] = []
    for m in SHELL_BLOCK_RE.finditer(text):
        for line in m.group("body").splitlines():
            line = line.rstrip()
            if line.startswith("dragonfly> "):
                invocations.append(line[len("dragonfly> "):].strip())
            elif line.startswith("$ redis-cli "):
                invocations.append(line[len("$ redis-cli "):].strip())
    return invocations


@dataclass
class DockerSession:
    container: str
    tag: str

    def exec(self, argv: list[str]) -> tuple[str, str, int]:
        full = ["docker", "exec", self.container, "redis-cli", "--no-raw"] + argv
        p = subprocess.run(full, capture_output=True, text=True)
        return p.stdout.rstrip(), p.stderr.rstrip(), p.returncode


def boot_docker(tag: str, emulated_cluster: bool = False,
                skip_pull: bool = False) -> DockerSession:
    image_ref = f"{DRAGONFLY_IMAGE}:{tag}"
    if not skip_pull:
        run(["docker", "pull", image_ref], check=False)
    container = f"dfly-docs-sync-{tag.replace('.', '-')}-{os.getpid()}"
    args = ["docker", "run", "-d", "--name", container, image_ref]
    if emulated_cluster:
        args.append("--cluster_mode=emulated")
    run(args)
    deadline = time.time() + PING_TIMEOUT_S
    while time.time() < deadline:
        p = run(["docker", "exec", container, "redis-cli", "PING"], check=False)
        if p.returncode == 0 and "PONG" in p.stdout:
            return DockerSession(container=container, tag=tag)
        time.sleep(0.3)
    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
    raise RuntimeError(f"Dragonfly {tag} did not respond to PING")


def kill_docker(session: DockerSession) -> None:
    subprocess.run(["docker", "rm", "-f", session.container],
                   capture_output=True)


def verify_invocations(session: DockerSession,
                       invocations: list[str]) -> list[dict]:
    """Run each invocation and capture the actual output. Returns a list of
    {invocation, stdout, stderr, returncode}."""
    out: list[dict] = []
    for inv in invocations:
        argv = inv.split()
        stdout, stderr, rc = session.exec(argv)
        out.append({
            "invocation": inv,
            "stdout": stdout,
            "stderr": stderr,
            "returncode": rc,
            "ok": rc == 0,
        })
    return out


def normalize_for_compare(text: str) -> list[str]:
    """Reduce text to the sequence of its non-blank lines, with each line's
    trailing whitespace stripped but internal whitespace preserved.

    Two texts that compare equal under this normalization differ ONLY in
    blank-line counts and/or trailing-whitespace — i.e. they are
    semantically identical. Real edits change at least one non-blank line.
    """
    return [l.rstrip() for l in text.split("\n") if l.strip()]


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

    # ACL line: rule #4 says do not modify it. Take the input ACL line text
    # and confirm it appears verbatim in the output.
    in_acl = re.search(
        r"^[ \t]*[\-*]?[ \t]*\*\*ACL[ \t]+categor(?:y|ies):\*\*[^\n]*",
        input_md, re.MULTILINE | re.IGNORECASE,
    )
    if in_acl:
        if in_acl.group(0).rstrip() not in output_md:
            errors.append(
                "ACL categories line was modified (rule #4 — owned by acl_sync.py)"
            )

    return errors


def verify_and_substitute_examples(
    text: str, session: DockerSession,
) -> tuple[str, list[dict], list[str]]:
    """Walk every ```shell``` block, run each `dragonfly>` invocation in
    Docker, and substitute the lines following each invocation with the
    actual output. Returns (new_text, errors, notes).

    `FLUSHALL` is issued before every block so one example's keyspace
    state cannot leak into another. Within a block, commands share state
    (each subsequent `dragonfly>` line sees the keyspace left by the
    previous one), which is what lets an example chain a SET and a GET.

    `errors` is a list of {invocation, rc, stderr} for non-zero exits.
    `notes` is a flat list of human-readable strings about the verification.
    """
    errors: list[dict] = []
    notes: list[str] = []
    out_parts: list[str] = []
    last_pos = 0
    invocation_count = 0
    block_count = 0

    for m in SHELL_BLOCK_RE.finditer(text):
        out_parts.append(text[last_pos:m.start()])
        # Clean slate per block. The reset is invisible to the reader of
        # the doc — they just see each block start from an empty keyspace.
        session.exec(["FLUSHALL"])
        block_count += 1
        body = m.group("body").rstrip("\n")
        lines = body.split("\n")
        rebuilt: list[str] = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if not line.startswith("dragonfly> "):
                # Lines before the first dragonfly> get passed through
                # (e.g. comments at the start of a block).
                rebuilt.append(line)
                i += 1
                continue
            cmd = line[len("dragonfly> "):].strip()
            argv = cmd.split()
            stdout, stderr, rc = session.exec(argv)
            invocation_count += 1
            rebuilt.append(line)
            actual = stdout if stdout else stderr
            if actual:
                rebuilt.extend(actual.split("\n"))
            if rc != 0:
                errors.append({
                    "invocation": cmd,
                    "rc": rc,
                    "stderr": stderr,
                })
            # Skip the LLM's predicted output — keep walking until next
            # `dragonfly>` line or end of block.
            j = i + 1
            while j < len(lines) and not lines[j].startswith("dragonfly> "):
                j += 1
            i = j
        new_block = "```shell\n" + "\n".join(rebuilt) + "\n```"
        out_parts.append(new_block)
        last_pos = m.end()

    out_parts.append(text[last_pos:])
    new_text = "".join(out_parts)

    if invocation_count:
        notes.append(
            f"verified {invocation_count} `dragonfly>` invocation(s) in "
            f"{block_count} block(s) (FLUSHALL between blocks)"
            + (f"; {len(errors)} non-zero exit(s)" if errors else "")
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
   block (existing or new) is verified in Docker by the caller AFTER you
   produce the markdown. The caller will replace the lines following
   each `dragonfly>` line with the actual server output.

   The caller issues `FLUSHALL` BEFORE each ```shell``` block so each
   block starts from a clean keyspace — prior examples never leak into
   the next one. Within a single block, state persists between
   consecutive `dragonfly>` lines, so `SET k 1` followed by `GET k`
   works as a chain.

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
       every invocation either way.
     * Do not invent commands you cannot justify from the source or
       runtime facts.
4. **Do NOT modify the `**ACL categor(y|ies):**` line.** That metadata
   is owned by a separate tool (`acl_sync.py`). Leave it byte-identical
   to what is in the input page — same prefix (with or without leading
   dash), same category list, same order.
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

The caller verifies every `dragonfly>` invocation in your `markdown` by
running it in a Docker container and substituting the captured output
in place of whatever output you wrote. So you do not have to predict
exact server output — but you DO have to put each example in the
correct section (no appending blocks just to host examples).
"""


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
        "=== docker_verified_examples (existing examples already verified) ===",
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


def update_one_file(
    entry: dict,
    after_tag: str,
    facts: dict,
    src: Path,
    skip_pull: bool,
    dry_run: bool,
) -> dict:
    """Update one file. Returns a result record."""
    rel = entry["path"]
    abs_path = REPO_ROOT / rel
    result: dict = {
        "path": rel,
        "status": "pending",
        "reason_input": entry.get("reason", ""),
        "notes": [],
    }
    if not abs_path.exists():
        result["status"] = "missing"
        result["error"] = f"file not found: {rel}"
        return result

    page_text = abs_path.read_text(encoding="utf-8")
    h1 = extract_h1(page_text)
    command = h1.upper() if h1 else None
    facts_entry = facts.get("data", {}).get("commands", {}).get(command)
    acl_cats = facts.get("data", {}).get("command_acl", {}).get(command, [])
    handler_info = (find_command_handler_source(src, command) if command else None)

    invocations = extract_redis_invocations(page_text)
    docker_examples: list[dict] = []
    session = None
    is_command_page = bool(facts_entry)
    needs_docker = bool(invocations) or is_command_page

    if needs_docker:
        emu = needs_emulated_cluster(handler_info, command)
        try:
            session = boot_docker(after_tag, emulated_cluster=emu,
                                  skip_pull=skip_pull)
        except Exception as e:
            result["notes"].append(f"docker boot failed: {e}; "
                                   f"verifying examples skipped")
            session = None
    if session and invocations:
        docker_examples = verify_invocations(session, invocations)

    try:
        try:
            import anthropic
        except ImportError:
            result["status"] = "skipped"
            result["error"] = "anthropic SDK not installed"
            return result
        if not os.getenv("ANTHROPIC_API_KEY"):
            result["status"] = "skipped"
            result["error"] = "ANTHROPIC_API_KEY not set"
            return result
        client = anthropic.Anthropic()
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
        print(f"  -> {rel}: calling Claude...")
        parsed, usage = call_llm_streaming(
            client, UPDATE_SYSTEM, user_text, UPDATE_MAX_TOKENS,
            f"update_{re.sub(r'[^a-z0-9]+', '_', rel.lower())[:60]}",
        )
        print(f"     tokens: in={usage['input_tokens']} "
              f"out={usage['output_tokens']}")
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
            LLM_DEBUG_DIR.mkdir(parents=True, exist_ok=True)
            ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            slug = re.sub(r"[^a-z0-9]+", "_", rel.lower())[:60]
            debug = LLM_DEBUG_DIR / f"docs_sync_rejected_{slug}_{ts}.md"
            debug.write_text(new_md, encoding="utf-8")
            result["status"] = "failed"
            result["error"] = (
                f"structural validation failed: {struct_errors}; "
                f"raw LLM markdown saved to "
                f"{debug.relative_to(REPO_ROOT)}"
            )
            return result

        # Verify every `dragonfly>` invocation in the LLM's markdown — both
        # the existing examples and any new ones the LLM placed in their
        # proper section — by running each in Docker and substituting the
        # actual output.
        if session:
            new_md, exec_errors, exec_notes = verify_and_substitute_examples(
                new_md, session,
            )
            result["notes"].extend(exec_notes)
            if exec_errors:
                result["notes"].append(
                    f"{len(exec_errors)} invocation(s) had non-zero exit; "
                    f"server output (stderr) substituted as the example "
                    f"output: {[e['invocation'] for e in exec_errors[:5]]}"
                    + ("..." if len(exec_errors) > 5 else "")
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

        if not dry_run:
            abs_path.write_text(new_md, encoding="utf-8")
        result["status"] = "updated"
    finally:
        if session:
            kill_docker(session)
    return result


def update_phase(plan: dict, after_tag: str, skip_pull: bool, dry_run: bool,
                 filter_glob: str = "") -> list[dict]:
    print(f"\n[Phase 2] Update {len(plan['files_to_update'])} file(s) "
          f"against tag {after_tag}")
    src = ensure_dragonfly_checkout(after_tag)

    # Load facts
    facts_path = FACTS_DIR / f"{after_tag}.json"
    if not facts_path.exists():
        print(f"  capturing facts via dfly_facts.py...")
        cmd = ["python3", str(DFLY_FACTS), "--tag", after_tag]
        if skip_pull:
            cmd.append("--skip-pull")
        subprocess.run(cmd, check=True)
    facts = json.loads(facts_path.read_text(encoding="utf-8"))

    results: list[dict] = []
    entries = plan["files_to_update"]
    if filter_glob:
        entries = [e for e in entries if fnmatch(e["path"], filter_glob)]
    for entry in entries:
        try:
            results.append(update_one_file(
                entry, after_tag, facts, src, skip_pull, dry_run,
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
                    help="Glob to limit which md files are processed.")
    ap.add_argument("--discover-only", action="store_true",
                    help="Run Phase 1 only; print the plan and exit.")
    ap.add_argument("--update-only-from", type=Path,
                    help="Skip Phase 1; load this saved plan JSON and run "
                         "Phase 2 against it.")
    ap.add_argument("--skip-pull", action="store_true",
                    help="Skip docker pull for the Dragonfly image.")
    ap.add_argument("--dry-run", action="store_true",
                    help="Do not write any updated files.")
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
        plan = discover_phase(args.before, args.after, also, args.filter)
        if args.discover_only:
            print("\n--- Plan summary ---")
            for entry in plan["files_to_update"]:
                print(f"  {entry['path']}")
                print(f"    reason: {entry.get('reason', '')}")
            return 0
        after_tag = args.after

    results = update_phase(plan, after_tag, args.skip_pull, args.dry_run,
                           args.filter)

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
