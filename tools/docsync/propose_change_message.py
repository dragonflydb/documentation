#!/usr/bin/env python3
"""propose_change_message.py — Suggest a commit/PR title + description for
the current working-tree changes.

Reads the git diff (working tree by default, or staged / against a base ref),
including untracked files, and asks Claude for a tight conventional-commit
title plus a Markdown body suitable for both `git commit -m` and
`gh pr create --body`.

The tool **never** runs git or gh commands itself. It writes the proposed
message to `tools/generated/change_messages/<timestamp>.md` and prints it
to stdout.

Usage:
    python tools/docsync/propose_change_message.py
    python tools/docsync/propose_change_message.py --staged
    python tools/docsync/propose_change_message.py --base origin/main
    python tools/docsync/propose_change_message.py --dump-prompt
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import anthropic

REPO_ROOT = Path(__file__).resolve().parents[2]
MESSAGES_DIR = REPO_ROOT / "tools" / "generated" / "change_messages"

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 1500
DIFF_BUDGET = 60_000  # rough char cap on the diff sent to the model


# --- Git helpers -------------------------------------------------------------

def run_git(args: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git"] + args, cwd=REPO_ROOT,
                          capture_output=True, text=True, check=check)


def diff_text(scope: str, base: str | None) -> tuple[str, list[str]]:
    """Return (diff_text, changed_paths). For working-tree scope this also
    appends untracked files to `changed_paths` (with a synthetic /dev/null
    diff in `diff_text`) so newly-created pages aren't invisible to the
    message writer."""
    if base:
        diff_args = ["diff", f"{base}...HEAD"]
        files_args = ["diff", "--name-only", f"{base}...HEAD"]
    elif scope == "staged":
        diff_args = ["diff", "--cached"]
        files_args = ["diff", "--cached", "--name-only"]
    else:  # working tree (staged + unstaged)
        diff_args = ["diff", "HEAD"]
        files_args = ["diff", "HEAD", "--name-only"]
    diff = run_git(diff_args, check=False).stdout
    files = [l for l in run_git(files_args, check=False).stdout.splitlines() if l]

    if not base and scope != "staged":
        untracked = [
            l for l in run_git(
                ["ls-files", "--others", "--exclude-standard"], check=False,
            ).stdout.splitlines() if l
        ]
        for u in untracked:
            if u in files:
                continue
            files.append(u)
            try:
                content = (REPO_ROOT / u).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                content = "(binary or unreadable)"
            diff += (
                f"\ndiff --git a/{u} b/{u}\nnew file\n--- /dev/null\n+++ b/{u}\n"
                + "".join(f"+{ln}\n" for ln in content.splitlines())
            )
    return diff, files


def status_lines() -> list[str]:
    return [l for l in run_git(["status", "--short"]).stdout.splitlines() if l]


def stat_summary(scope: str, base: str | None) -> str:
    if base:
        args = ["diff", "--stat", f"{base}...HEAD"]
    elif scope == "staged":
        args = ["diff", "--cached", "--stat"]
    else:
        args = ["diff", "HEAD", "--stat"]
    return run_git(args, check=False).stdout


def categorize(files: list[str]) -> dict[str, list[str]]:
    """Bucket changed files for an at-a-glance summary in the prompt."""
    buckets = {
        "command_ref":   [],
        "managing":      [],
        "other_docs":    [],
        "tooling":       [],
        "other":         [],
    }
    for f in files:
        if f.startswith("docs/command-reference/"):
            buckets["command_ref"].append(f)
        elif f.startswith("docs/managing-dragonfly/"):
            buckets["managing"].append(f)
        elif f.startswith("docs/"):
            buckets["other_docs"].append(f)
        elif f.startswith("tools/"):
            buckets["tooling"].append(f)
        else:
            buckets["other"].append(f)
    return buckets


# --- Prompt construction -----------------------------------------------------

WRITER_SYSTEM = """\
You write commit messages and PR descriptions for documentation changes in
the Dragonfly DB docs repo.

Output format — strict JSON only:

  {
    "title": "<conventional-commit subject, <=70 chars>",
    "body":  "<Markdown body with ## Summary and ## Test plan sections>"
  }

Hard constraints:
- Title in conventional-commits style: `docs: fix ACL ...`, `docs: update flag defaults`, etc.
- No leading articles ("the", "a"), no period at the end, lowercase after `docs:`.
- Body: ## Summary (1–3 bullets) and ## Test plan (markdown checklist).
- Don't speculate beyond what the diff justifies.
- Don't promise features that aren't in the diff.
- No emojis, no co-author trailers, no boilerplate.
- If multiple unrelated change types are mixed, mention each briefly.
- Output JSON only — no prose before or after.
"""


def build_user_text(
    diff: str, status: list[str], stats: str,
    buckets: dict[str, list[str]],
) -> str:
    parts: list[str] = []
    parts.append("=== git status (--short) ===")
    parts.append("\n".join(status) or "(clean)")
    parts.append("")
    parts.append("=== diff --stat ===")
    parts.append(stats.strip() or "(no diff)")
    parts.append("")
    if any(buckets.values()):
        parts.append("=== Files by bucket ===")
        for k, fs in buckets.items():
            if fs:
                parts.append(f"{k} ({len(fs)}):")
                parts.extend(f"  {f}" for f in fs)
        parts.append("")
    parts.append("=== Diff ===")
    if len(diff) > DIFF_BUDGET:
        parts.append(diff[:DIFF_BUDGET])
        parts.append(f"\n…(diff truncated at {DIFF_BUDGET:,} chars; "
                     f"original {len(diff):,} chars)…")
    else:
        parts.append(diff)
    parts.append("")
    parts.append("=== Task ===")
    parts.append("Produce the JSON {title, body} now. Output JSON only.")
    return "\n".join(parts)


def call_llm(client: anthropic.Anthropic, user_text: str) -> tuple[dict, dict]:
    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=[{"type": "text", "text": WRITER_SYSTEM,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_text}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1] if "\n" in text else text
        text = text.rsplit("```", 1)[0]
    parsed = json.loads(text)
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }
    return parsed, usage


# --- Atomic write ------------------------------------------------------------

def write_atomic(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


# --- Main --------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--staged", action="store_true",
                   help="Describe only --cached (staged) diff.")
    g.add_argument("--base", help="Describe diff <base>...HEAD (e.g. origin/main).")
    ap.add_argument("--dump-prompt", action="store_true",
                    help="Write the prompt and exit without calling the LLM.")
    args = ap.parse_args()

    scope = "staged" if args.staged else "worktree"
    diff, files = diff_text(scope, args.base)
    if not files and not diff.strip():
        print("Nothing to describe (empty diff).")
        return 0

    status = status_lines()
    stats = stat_summary(scope, args.base)
    buckets = categorize(files)

    user_text = build_user_text(diff, status, stats, buckets)

    if args.dump_prompt:
        prompt_path = MESSAGES_DIR / "_last.prompt.md"
        write_atomic(
            prompt_path,
            f"=== SYSTEM ===\n{WRITER_SYSTEM}\n\n=== USER ===\n{user_text}\n",
        )
        print(f"Wrote prompt: {prompt_path.relative_to(REPO_ROOT)}")
        return 0

    print(f"Files in scope: {len(files)}")
    print("Calling Claude...")
    client = anthropic.Anthropic()
    msg, usage = call_llm(client, user_text)
    print(f"  tokens: in={usage['input_tokens']} out={usage['output_tokens']} "
          f"stop={usage['stop_reason']}")

    title = msg.get("title", "").strip()
    body = msg.get("body", "").strip()
    rendered = f"{title}\n\n{body}\n"
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_path = MESSAGES_DIR / f"{ts}.md"
    write_atomic(out_path, rendered)

    print("\n" + "=" * 70)
    print(f"# Title:\n{title}")
    print("\n# Body:")
    print(body)
    print("=" * 70)
    print(f"\nSaved to {out_path.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
