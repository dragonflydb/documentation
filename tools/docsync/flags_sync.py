#!/usr/bin/env python3
"""flags_sync.py — Synchronize docs/managing-dragonfly/flags.md with reality.

Three-stage pipeline:

  1. Capture facts. Two sources:
       a) Docker (`dfly_facts.py`) — authoritative for default values, types,
          groups, and the short ABSL_FLAG help string.
       b) Source code (parsed inline) — provides the ABSL_FLAG declaration's
          file/line, surrounding C++ comment block, and (when the flag's type
          is an enum) the enum's value list with comments. This is what gives
          the LLM enough context to write quality descriptions for new flags
          and to expand enum-typed defaults like `compression_mode = 3` into
          something a reader can actually understand.

  2. Mechanical pass.
     a) Delete sections for flags the server no longer reports (the binary
        is the authoritative source — if a flag isn't there the doc was
        wrong).
     b) For each remaining flag, replace the single `default: ...` line if
        the value differs. A byte-equivalence check skips cosmetic
        reformatting (`0` vs `0B`, `128MiB` vs `128.00MiB`).
     **Enum-typed defaults** (doc has a number, server reports an uppercase
     enum constant) are NOT mechanically rewritten — keeping the integer is
     better for the CLI reader, and the LLM polish is responsible for adding
     the enum-value table to the description.

  3. LLM polish. Claude receives the mechanically-fixed page (already with
     obsolete flags removed and defaults updated), the ground-truth dict
     restricted to flags that should be in the output, the source-code data
     per flag, and explicit instructions: add missing flags using their
     ABSL_FLAG help and any surrounding C++ comment context; for enum-typed
     defaults, expand the description with a value table; preserve
     human-written content. The output is validated (every flag present,
     defaults match modulo equivalence, no duplicates) — if validation
     fails the LLM output is discarded and the mechanical-only result
     stays on disk. A post-process pass also auto-deduplicates flag
     sections in case the LLM emits stub copies.

Usage:
    python tools/docsync/flags_sync.py --tag v1.38.0
    python tools/docsync/flags_sync.py --tag v1.38.0 --dry-run
    python tools/docsync/flags_sync.py --tag v1.38.0 --no-llm
    python tools/docsync/flags_sync.py --tag v1.38.0 --skip-source
    python tools/docsync/flags_sync.py --facts tools/generated/facts/v1.38.0.json
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FLAGS_PAGE = REPO_ROOT / "docs" / "managing-dragonfly" / "flags.md"
FACTS_DIR = REPO_ROOT / "tools" / "generated" / "facts"
SOURCE_DIR = REPO_ROOT / "tools" / "generated" / "source"
DFLY_FACTS = REPO_ROOT / "tools" / "docsync" / "dfly_facts.py"

DRAGONFLY_REPO = "https://github.com/dragonflydb/dragonfly.git"
DRAGONFLY_CHECKOUT = Path("/tmp/dragonfly-docsync")

MODEL = "claude-sonnet-4-6"
MAX_TOKENS = 32000

SECTION_RE = re.compile(
    r"^###[ \t]+`--(?P<name>[a-z][a-z0-9_]*)`[ \t]*\n"
    r"(?P<body>.*?)(?=^###[ \t]+`--|\Z)",
    re.DOTALL | re.MULTILINE,
)
DEFAULT_RE = re.compile(r"`default:\s*(?P<v>[^`]*)`")

# Flags declared in upstream libraries are not part of Dragonfly's documented
# surface. They show up in --helpfull because Dragonfly statically links the
# glog / absl libraries, but they are general-purpose logging / argument
# plumbing flags (--v, --vmodule, --alsologtoemail, --colorlogtostdout,
# --symbolize_stacktrace, --fromenv, --tryfromenv, --undefok, ...). Hiding
# them from auto-add prevents the LLM polish from polluting flags.md with
# upstream-library noise.
UPSTREAM_GROUP_PREFIXES = (
    "glog-src/",
    "abseil_cpp-src/",
)


def run(cmd: list[str], cwd: Path | None = None,
        check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def filter_user_facing(flags: dict[str, dict]) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for name, info in flags.items():
        group = info.get("group") or ""
        if any(group.startswith(p) for p in UPSTREAM_GROUP_PREFIXES):
            continue
        out[name] = info
    return out


# --- Value-equivalence (so cosmetic byte reformatting isn't a fix) -----------

_BYTE_UNIT_TO_BYTES: dict[str, int] = {
    "":  1,  "b":   1,
    "k": 1024, "kb": 1024, "kib": 1024,
    "m": 1024 ** 2, "mb": 1024 ** 2, "mib": 1024 ** 2,
    "g": 1024 ** 3, "gb": 1024 ** 3, "gib": 1024 ** 3,
    "t": 1024 ** 4, "tb": 1024 ** 4, "tib": 1024 ** 4,
}
_BYTE_VALUE_RE = re.compile(r"^\s*(-?\d+(?:\.\d+)?)\s*([A-Za-z]*)\s*$")


def _parse_byte_value(s: str) -> int | None:
    m = _BYTE_VALUE_RE.match(s)
    if not m:
        return None
    unit = m.group(2).lower()
    if unit not in _BYTE_UNIT_TO_BYTES:
        return None
    return int(round(float(m.group(1)) * _BYTE_UNIT_TO_BYTES[unit]))


def values_equivalent(a: str, b: str) -> bool:
    """True if `a` and `b` represent the same value modulo byte-unit
    formatting (`0` == `0B`, `128MiB` == `128.00MiB`, `65536` == `64.0KiB`).
    Returns False for anything we cannot prove equal."""
    if a.strip() == b.strip():
        return True
    ab = _parse_byte_value(a)
    bb = _parse_byte_value(b)
    return ab is not None and ab == bb


_ENUM_NAME_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")
_INT_RE = re.compile(r"^-?\d+$")


def is_enum_change(doc: str, server: str) -> bool:
    """True if the doc has an integer default and the server reports an
    UPPERCASE_ENUM constant. We do NOT mechanically apply such changes —
    a number is a more useful default for a CLI reader, and the LLM polish
    will expand the description with the enum-value table."""
    return bool(_INT_RE.match(doc.strip()) and _ENUM_NAME_RE.match(server.strip()))


# --- Section parsing ---------------------------------------------------------

@dataclass
class FlagSection:
    name: str
    span: tuple[int, int]
    body: str
    default: str | None


@dataclass
class MechResult:
    fixed_defaults: list[tuple[str, str, str]] = field(default_factory=list)
    failed_defaults: list[tuple[str, str]] = field(default_factory=list)
    deferred_enum: list[tuple[str, str, str]] = field(default_factory=list)  # (name, doc, server)
    removed_from_doc: list[str] = field(default_factory=list)  # in doc, no longer on server — deleted
    missing_from_doc: list[str] = field(default_factory=list)


def parse_sections(text: str) -> dict[str, FlagSection]:
    out: dict[str, FlagSection] = {}
    for m in SECTION_RE.finditer(text):
        name = m.group("name")
        body = m.group("body")
        dm = DEFAULT_RE.search(body)
        default = dm.group("v").strip() if dm else None
        out[name] = FlagSection(
            name=name, span=(m.start(), m.end()),
            body=body, default=default,
        )
    return out


# --- Source code parsing (inline) -------------------------------------------

def ensure_dragonfly_checkout(tag: str, refresh: bool) -> Path:
    """Ensure /tmp/dragonfly-docsync is a clean checkout at `tag`."""
    if not (DRAGONFLY_CHECKOUT / ".git").exists():
        DRAGONFLY_CHECKOUT.parent.mkdir(parents=True, exist_ok=True)
        print(f"  cloning Dragonfly source to {DRAGONFLY_CHECKOUT}...")
        run(["git", "clone", "--quiet", DRAGONFLY_REPO, str(DRAGONFLY_CHECKOUT)])
    if refresh:
        run(["git", "fetch", "--tags", "--quiet"], cwd=DRAGONFLY_CHECKOUT, check=False)
    # `git checkout <tag>` is idempotent and quiet
    run(["git", "checkout", "--quiet", tag], cwd=DRAGONFLY_CHECKOUT, check=False)
    return DRAGONFLY_CHECKOUT


def _split_top_level_commas(body: str) -> list[int]:
    """Indices of `,` at paren depth 0, ignoring chars in strings/chars."""
    out: list[int] = []
    depth = 0
    in_str: str | None = None
    i = 0
    while i < len(body):
        c = body[i]
        if in_str:
            if c == "\\" and i + 1 < len(body):
                i += 2
                continue
            if c == in_str:
                in_str = None
        elif c in ('"', "'"):
            in_str = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
        elif c == "," and depth == 0:
            out.append(i)
        i += 1
    return out


def _find_matching_paren(text: str, open_pos: int) -> int:
    """Return position of `)` matching `(` at open_pos, or -1."""
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
        elif c in ('"', "'"):
            in_str = c
        elif c == "(":
            depth += 1
        elif c == ")":
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


_STRING_LITERAL_RE = re.compile(r'"((?:[^"\\]|\\.)*)"', re.DOTALL)


def _join_string_literals(s: str) -> str:
    """Concatenate adjacent C++ string literals: `"foo" "bar"` -> `foobar`."""
    parts = _STRING_LITERAL_RE.findall(s)
    if not parts:
        return s.strip().strip(';').strip()
    # Unescape \n, \t, \\
    joined = "".join(p for p in parts)
    return re.sub(r"\\(.)", r"\1", joined)


def _comments_above(text: str, line_start: int) -> str:
    """Collect contiguous `// ...` lines and `/* ... */` block above `line_start`."""
    lines_before = text[:line_start].split("\n")
    out: list[str] = []
    in_block = False
    for line in reversed(lines_before):
        stripped = line.strip()
        if not out and stripped == "":
            continue
        if stripped.startswith("//"):
            out.insert(0, stripped[2:].strip())
            continue
        if stripped.endswith("*/"):
            out.insert(0, stripped)
            in_block = True
            continue
        if in_block:
            out.insert(0, stripped)
            if stripped.startswith("/*"):
                in_block = False
            continue
        break
    return "\n".join(out)


def parse_absl_flags(text: str) -> list[dict]:
    """Yield each ABSL_FLAG declaration as
    {name, type, default_expr, description, comments, line}."""
    out: list[dict] = []
    for m in re.finditer(r"\bABSL_FLAG\s*\(", text):
        open_paren = m.end() - 1
        close_paren = _find_matching_paren(text, open_paren)
        if close_paren < 0:
            continue
        body = text[open_paren + 1:close_paren]
        commas = _split_top_level_commas(body)
        if len(commas) < 3:
            continue
        type_str = body[:commas[0]].strip()
        name = body[commas[0] + 1:commas[1]].strip()
        default_expr = body[commas[1] + 1:commas[2]].strip()
        desc_raw = body[commas[2] + 1:].strip()
        if not name or not name.replace("_", "").isalnum():
            continue
        line_start = text.rfind("\n", 0, m.start()) + 1
        comments = _comments_above(text, line_start)
        out.append({
            "name": name,
            "type": type_str,
            "default_expr": default_expr,
            "description": _join_string_literals(desc_raw),
            "comments": comments,
            "line": text.count("\n", 0, m.start()) + 1,
        })
    return out


def parse_enum_definitions(text: str) -> dict[str, list[dict]]:
    """Find `enum [class] Name [: type] { values };` blocks. Return
    {name: [{name, value, comment}, ...]}.

    For implicit enum values (no `= N`), assign the standard C++ positional
    value (0 for the first, prev+1 thereafter). When a value is explicit
    we record the source expression as a string and resume incrementing
    from the parsed integer if the expression is a plain integer.
    """
    out: dict[str, list[dict]] = {}
    pat = re.compile(
        r"\benum\s+(?:class\s+|struct\s+)?(?P<name>[A-Z][A-Za-z0-9_]*)"
        r"(?:\s*:\s*[\w:]+)?\s*\{(?P<body>[^}]*)\}\s*;",
        re.DOTALL,
    )
    for m in pat.finditer(text):
        body = m.group("body")
        values: list[dict] = []
        next_implicit = 0
        for raw in body.split(","):
            line = raw.strip()
            if not line:
                continue
            comment = ""
            cmt_m = re.search(r"//(.*)$", line)
            if cmt_m:
                comment = cmt_m.group(1).strip()
                line = line[:cmt_m.start()].rstrip()
            if "=" in line:
                nm, _, vl = line.partition("=")
                vl = vl.strip()
                # If the value is a plain integer, use it & resume incrementing.
                try:
                    next_implicit = int(vl, 0) + 1
                    value_str = vl
                except ValueError:
                    value_str = vl  # leave non-integer expression as-is
                values.append({"name": nm.strip(), "value": value_str, "comment": comment})
            else:
                values.append({"name": line.strip(), "value": str(next_implicit),
                               "comment": comment})
                next_implicit += 1
        if values:
            out[m.group("name")] = values
    return out


def _enum_type_token(type_str: str) -> str | None:
    """For type strings like `dfly::CompressionMode`, return `CompressionMode`.
    For primitive types (bool, int, std::string) return None."""
    bare = type_str.split("::")[-1].strip().rstrip("&*")
    if bare in {"bool", "int", "int32_t", "int64_t", "uint32_t", "uint64_t",
                "uint16_t", "uint8_t", "size_t", "double", "float", "string"}:
        return None
    if not re.match(r"^[A-Z][A-Za-z0-9_]*$", bare):
        return None
    return bare


def extract_source_facts(
    src: Path, target_names: set[str], verbose: bool = True,
) -> dict[str, dict]:
    """Scan dragonfly source, return {flag_name: {file, line, type,
    default_expr, description, comments, enum_values?}} for every
    ABSL_FLAG whose name is in `target_names`."""
    if verbose:
        print(f"  scanning C++ source under {src}...")
    grep = subprocess.run(
        ["grep", "-rln", "ABSL_FLAG", str(src),
         "--include=*.cc", "--include=*.h"],
        capture_output=True, text=True, check=False,
    )
    files = [Path(p) for p in grep.stdout.splitlines() if p]
    flags: dict[str, dict] = {}
    enum_pool: dict[str, list[dict]] = {}
    for f in files:
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for decl in parse_absl_flags(text):
            if decl["name"] not in target_names:
                continue
            decl["file"] = str(f.relative_to(src))
            flags[decl["name"]] = decl
        enum_pool.update(parse_enum_definitions(text))
    # Also walk header files that didn't contain ABSL_FLAG (for enums).
    for f in src.rglob("*.h"):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        enum_pool.update(parse_enum_definitions(text))
    for name, info in flags.items():
        token = _enum_type_token(info["type"])
        if token and token in enum_pool:
            info["enum_values"] = enum_pool[token]
            info["enum_name"] = token
    if verbose:
        with_enum = sum(1 for v in flags.values() if "enum_values" in v)
        print(f"  parsed {len(flags)} ABSL_FLAG declaration(s); "
              f"{with_enum} have an enum-typed default")
    return flags


def load_or_capture_source(args: argparse.Namespace,
                           target_names: set[str]) -> dict[str, dict]:
    cache = SOURCE_DIR / f"{args.tag}.json"
    if cache.exists() and not args.refresh_source:
        cached = json.loads(cache.read_text(encoding="utf-8"))
        # Cache covers all flags; intersect with current targets
        return {n: cached[n] for n in target_names if n in cached}
    src = ensure_dragonfly_checkout(args.tag, refresh=args.refresh_source)
    facts = extract_source_facts(src, target_names)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    tmp = cache.with_suffix(cache.suffix + ".tmp")
    tmp.write_text(
        json.dumps(facts, indent=2, sort_keys=True, ensure_ascii=False),
        encoding="utf-8",
    )
    os.replace(tmp, cache)
    return facts


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


# --- Mechanical pass ---------------------------------------------------------

def patch_default(text: str, section: FlagSection, new_default: str) -> str | None:
    s, e = section.span
    section_text = text[s:e]
    new_section, count = DEFAULT_RE.subn(
        f"`default: {new_default}`", section_text, count=1,
    )
    if count != 1:
        return None
    return text[:s] + new_section + text[e:]


def mechanical_pass(
    text: str,
    all_server_flags: dict[str, dict],
    user_facing_flags: dict[str, dict],
) -> tuple[str, MechResult]:
    """Two stages on the page text:
      1. Remove sections for flags the server no longer reports — these are
         obsolete and the server is the authoritative source.
      2. Fix `default: ...` lines for the remaining flags whose default
         value drifted.
    """
    result = MechResult()
    sections = parse_sections(text)

    doc_names = set(sections.keys())
    all_server_names = set(all_server_flags.keys())
    user_facing_names = set(user_facing_flags.keys())

    result.missing_from_doc = sorted(user_facing_names - doc_names)
    result.removed_from_doc = sorted(doc_names - all_server_names)

    # Stage 1: delete obsolete sections. Walk in reverse position so earlier
    # spans remain valid as we mutate the text.
    if result.removed_from_doc:
        for name in sorted(result.removed_from_doc,
                           key=lambda n: -sections[n].span[0]):
            s, e = sections[name].span
            text = text[:s] + text[e:]
        # Re-parse for stage 2 since spans have shifted.
        sections = parse_sections(text)

    # Stage 2: fix defaults for flags still in both doc and server.
    remaining = set(sections.keys()) & all_server_names
    for name in sorted(remaining, key=lambda n: -sections[n].span[0]):
        sec = sections[name]
        server_default = all_server_flags[name].get("default", "")
        if sec.default is None:
            result.failed_defaults.append((name, "section has no `default: ...` line"))
            continue
        if values_equivalent(sec.default, server_default):
            continue
        if is_enum_change(sec.default, server_default):
            # Defer: keep the integer in `default:`, let the LLM polish add
            # an enum-value table to the description instead.
            result.deferred_enum.append((name, sec.default, server_default))
            continue
        new_text = patch_default(text, sec, server_default)
        if new_text is None:
            result.failed_defaults.append(
                (name, "could not substitute `default:` (matches != 1)"),
            )
            continue
        text = new_text
        result.fixed_defaults.append((name, sec.default, server_default))

    return text, result


# --- LLM polish --------------------------------------------------------------

POLISH_SYSTEM = """\
You are polishing a Dragonfly DB flag-reference page (docs/managing-dragonfly/flags.md).

You will receive:
  - The current page (already mechanically reconciled — every default value
    you see for an existing flag has been pre-fixed and is authoritative).
  - `must_be_present`: the EXACT list of flag names whose `### `--<name>``
    section must appear in the output. Not a subset, not a superset —
    EXACTLY this list. Treat it as the closed-world set.
  - `ground_truth`: dict { flag_name -> { default, description, type, group } }
    captured from the running binary's `--helpfull`. Restricted to
    `must_be_present` plus a few flags the page already documents that the
    server still reports. `description` is verbatim help text.
  - `source_facts`: dict { flag_name -> { type, default_expr, description,
    comments, file, line, enum_name?, enum_values? } } captured from the
    Dragonfly C++ source. Restricted to the same set as `ground_truth`.
    `comments` are the C++ comments immediately above the ABSL_FLAG
    declaration; they often contain rationale. `enum_values` is present
    only when the flag's type is an enum; each entry has { name, value,
    comment }.
  - `flags_to_add`: subset of `must_be_present` — flags the server reports
    that are NOT yet in the page; you must write new sections for these.
  - `enum_defaults_to_expand`: list of { flag, doc_default, server_default }.
    For each, the page's `default:` MUST stay as the integer (it is what the
    CLI accepts). The flag's description in the polished page MUST list the
    enum's values, e.g.:

        `default: 3`

        Where:
        - `0` — `NONE` — single-entry, no compression.
        - `2` — `SINGLE_ENTRY_LZ4` — ...
        - `3` — `MULTI_ENTRY_LZ4` — ...

    Use the `enum_values` data from `source_facts` to populate the table;
    do NOT invent a meaning that's not in the comments or enum names.

Hard rules:
  1. The output MUST contain a `### `--<name>`` section for EXACTLY the
     flags in `must_be_present`. Adding a flag not in this list is a
     fatal error. Omitting one is a fatal error. The set must match
     character-for-character.
  2. Every `default: X` line in the output MUST equal `ground_truth[name].default`
     (modulo byte-equivalence — `0` ≡ `0B`, `128MiB` ≡ `128.00MiB`).
     EXCEPTION: for flags listed in `enum_defaults_to_expand`, the
     `default:` line MUST be the integer `doc_default` (e.g. `3`), NOT the
     enum name. The enum name and meaning go in the description body.
  3. For flags already documented: prefer the existing description. If the
     `--helpfull` text or `source_facts.comments` adds useful detail not
     already covered, integrate it sparingly. Do not rewrite for style.
  4. For flags in `flags_to_add`: write a clear, neutral description using
     `--helpfull` text + `source_facts.comments`. Do not invent capabilities
     beyond what those texts say.
  5. Preserve every non-flag piece (intro paragraphs, headings, examples).
  6. Section ordering: keep already-present flags in their current positions.
     Place newly-added flags near related flags (by `group`) when an obvious
     anchor exists; otherwise at the end of `## Available Flags`.
  7. Each flag MUST appear EXACTLY ONCE. Do NOT emit "see above" stubs,
     consolidated index sections, or any duplicate `### `--<name>`` headers.
     The output is parsed by counting `### `--name`` occurrences; two for
     the same name fails the check. If you find yourself tempted to
     reference a flag again later in the page, instead leave just the
     single canonical section and link to it from surrounding prose.

Your response MUST be a single JSON object and NOTHING else. The very first
character of your response must be `{` and the very last must be `}`. No
preamble like "I'll analyze the inputs", no closing remark, no markdown
fences (```), no explanation. The schema:

  { "markdown": "<full file content>",
    "notes":    ["<short bullet about decisions you made>", ...] }

If you violate this format the downstream parser will discard your work.
"""


def _extract_json_object(text: str) -> dict | None:
    """Best-effort extraction of a top-level JSON object from `text`.

    Handles the common LLM failure modes:
      * verbatim JSON (no wrapping)               -> json.loads(text)
      * preamble before / after the JSON          -> slice between first { and matching }
      * ```json ... ``` fence                     -> extract fenced block
    Returns the parsed dict, or None if nothing parseable was found.
    """
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
                candidate = text[start:i + 1]
                try:
                    return json.loads(candidate)
                except json.JSONDecodeError:
                    start = -1
        i += 1
    return None


def call_llm(client, system_prompt: str, user_text: str) -> tuple[dict, dict]:
    # Streaming is required because the Anthropic SDK refuses non-streaming
    # requests that may exceed 10 minutes of generation time, which a 32K
    # max_tokens polish on the full flags page reliably hits.
    text_parts: list[str] = []
    chars = 0
    print("  streaming response", end="", flush=True)
    with client.messages.stream(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=[{"type": "text", "text": system_prompt,
                 "cache_control": {"type": "ephemeral"}}],
        messages=[{"role": "user", "content": user_text}],
    ) as stream:
        for chunk in stream.text_stream:
            text_parts.append(chunk)
            chars += len(chunk)
            if chars % 4000 < len(chunk):  # roughly one dot per 4K chars
                print(".", end="", flush=True)
        response = stream.get_final_message()
    print(f" done ({chars} chars streamed)")
    text = "".join(text_parts).strip()
    if not text:
        # Streaming should always yield text; if not, fall back to scanning
        # the assembled message's content blocks just in case.
        for block in response.content:
            block_type = getattr(block, "type", None) or block.get("type")
            if block_type == "text":
                text += getattr(block, "text", "") or block.get("text", "")
        text = text.strip()
    if not text:
        raise RuntimeError(
            f"LLM returned no text content "
            f"(stop_reason={response.stop_reason}, "
            f"blocks={[getattr(b, 'type', None) for b in response.content]})"
        )
    parsed = _extract_json_object(text)
    if parsed is None:
        debug = SOURCE_DIR.parent / "llm_debug" / f"flags_polish_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.txt"
        debug.parent.mkdir(parents=True, exist_ok=True)
        debug.write_text(text, encoding="utf-8")
        raise RuntimeError(
            f"LLM response did not contain a parseable JSON object; "
            f"raw text saved to {debug.relative_to(REPO_ROOT)} for inspection. "
            f"stop_reason={response.stop_reason}, len={len(text)} chars."
        )
    usage = {
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
        "stop_reason": response.stop_reason,
    }
    return parsed, usage


def build_polish_user_text(
    page_text: str,
    ground_truth: dict[str, dict],
    source_facts: dict[str, dict],
    must_be_present: list[str],
    flags_to_add: list[str],
    enum_defaults_to_expand: list[dict],
) -> str:
    parts = [
        "=== must_be_present ===",
        "(closed-world set — output MUST have exactly these "
        f"`### `--<name>`` sections, no others, no duplicates; "
        f"{len(must_be_present)} flag(s))",
        json.dumps(must_be_present, indent=2),
        "",
        "=== ground_truth ===",
        json.dumps(ground_truth, indent=2, sort_keys=True, ensure_ascii=False),
        "",
        "=== source_facts ===",
        json.dumps(source_facts, indent=2, sort_keys=True, ensure_ascii=False),
        "",
        "=== flags_to_add ===",
        json.dumps(flags_to_add, indent=2),
        "",
        "=== enum_defaults_to_expand ===",
        json.dumps(enum_defaults_to_expand, indent=2),
        "",
        "=== current page ===",
        page_text,
        "",
        "=== task ===",
        "Produce the JSON {markdown, notes}. JSON only.",
    ]
    return "\n".join(parts)


# --- Validation --------------------------------------------------------------

def repair_stub_sections(
    polished: str, original: str,
) -> tuple[str, list[str]]:
    """Detect "stub" flag sections in `polished` (no `default:` line, often
    bodies like "Duplicate removed — see above" or "Intentionally omitted")
    and substitute the corresponding section from `original` if it has one.

    This guards against an LLM failure mode where the model self-polices
    against duplicates by replacing a real section with a stub, even though
    no actual duplicate exists.
    """
    polished_secs = parse_sections(polished)
    original_secs = parse_sections(original)

    candidates: list[tuple[str, tuple[int, int]]] = [
        (name, polished_secs[name].span)
        for name in polished_secs
        if polished_secs[name].default is None and name in original_secs
        and original_secs[name].default is not None
    ]
    candidates.sort(key=lambda x: -x[1][0])  # process highest position first

    text = polished
    repaired: list[str] = []
    for name, (s, e) in candidates:
        orig_s, orig_e = original_secs[name].span
        text = text[:s] + original[orig_s:orig_e] + text[e:]
        repaired.append(name)
    return text, repaired


_LENIENT_HEADER_RE = re.compile(
    r"^###[ \t]+`--(?P<name>[a-z][a-z0-9_]*)`[^\n]*\n",
    re.MULTILINE,
)


def deduplicate_sections(text: str) -> tuple[str, list[str]]:
    """Remove duplicate `### `--<name>`` sections, keeping the longest one
    (richest content). Returns (deduped_text, dropped_flag_names).

    Uses a lenient header regex that matches even when the LLM adds trailing
    text on the header line (e.g. `### `--foo` is defined above.`) — those
    stubs would otherwise hide from the strict SECTION_RE.
    """
    headers = list(_LENIENT_HEADER_RE.finditer(text))
    if not headers:
        return text, []
    grouped: dict[str, list[tuple[int, int]]] = {}
    for i, m in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        grouped.setdefault(m.group("name"), []).append((m.start(), end))
    drop_spans: list[tuple[int, int]] = []
    dropped: list[str] = []
    for name, spans in grouped.items():
        if len(spans) <= 1:
            continue
        # Keep the longest section; on tie, the earliest in the file.
        keep_idx = max(range(len(spans)),
                       key=lambda i: (spans[i][1] - spans[i][0], -spans[i][0]))
        for i, (s, e) in enumerate(spans):
            if i != keep_idx:
                drop_spans.append((s, e))
                dropped.append(name)
    drop_spans.sort(reverse=True)
    out = text
    for s, e in drop_spans:
        out = out[:s] + out[e:]
    return out, dropped


def restore_missing_sections(
    polished: str, original: str, must_be_present: set[str],
) -> tuple[str, list[str]]:
    """If a flag is in `must_be_present` AND was a real section in `original`
    (with a `default:` line) but is missing from `polished`, paste the
    original section into `polished` at a position close to where it lived
    in `original` (right after the closest preceding flag that is in both)."""
    polished_secs = parse_sections(polished)
    original_secs = parse_sections(original)

    missing = sorted(
        n for n in must_be_present
        if n in original_secs and original_secs[n].default is not None
        and n not in polished_secs
    )
    if not missing:
        return polished, []

    original_order = sorted(original_secs.keys(),
                            key=lambda n: original_secs[n].span[0])
    text = polished
    restored: list[str] = []
    for name in missing:
        s_orig, e_orig = original_secs[name].span
        section_text = original[s_orig:e_orig]
        # Find the closest preceding flag in original that is also currently
        # in `text`, and append after it.
        idx = original_order.index(name)
        anchor: str | None = None
        for j in range(idx - 1, -1, -1):
            if original_order[j] in parse_sections(text):
                anchor = original_order[j]
                break
        current = parse_sections(text)
        if anchor and anchor in current:
            anchor_s, anchor_e = current[anchor].span
            text = text[:anchor_e] + section_text + text[anchor_e:]
        else:
            first_h3 = _LENIENT_HEADER_RE.search(text)
            if first_h3:
                text = text[:first_h3.start()] + section_text + text[first_h3.start():]
            else:
                # No H3 anywhere — append at end (degenerate case).
                text = text.rstrip() + "\n\n" + section_text
        restored.append(name)
    return text, restored


def validate_polish(
    polished: str,
    all_server_flags: dict[str, dict],
    must_be_present: set[str],
    enum_default_keep_int: dict[str, str],   # name -> integer that must stay in `default:`
) -> list[str]:
    errors: list[str] = []
    # Duplicate-section detection has to run on the raw text — parse_sections
    # collapses duplicates (last one wins) so it cannot tell us by itself.
    head_counts: dict[str, int] = {}
    for n in re.findall(r"^###\s+`--([a-z][a-z0-9_]*)`", polished, re.MULTILINE):
        head_counts[n] = head_counts.get(n, 0) + 1
    dupes = sorted(n for n, c in head_counts.items() if c > 1)
    if dupes:
        errors.append(f"duplicate flag section(s): {dupes[:10]}"
                      f"{'...' if len(dupes) > 10 else ''}")
    found = parse_sections(polished)
    found_names = set(found.keys())

    missing = must_be_present - found_names
    if missing:
        errors.append(f"missing {len(missing)} flag(s) from output: "
                      f"{sorted(missing)[:10]}{'...' if len(missing) > 10 else ''}")

    unexpected = found_names - must_be_present
    if unexpected:
        errors.append(f"unexpected flag(s) added: "
                      f"{sorted(unexpected)[:10]}"
                      f"{'...' if len(unexpected) > 10 else ''}")

    for name, sec in sorted(found.items()):
        if name in enum_default_keep_int:
            expected = enum_default_keep_int[name]
            got = sec.default or ""
            if got.strip() != expected.strip():
                errors.append(
                    f"--{name}: enum-typed default should remain `{expected}` "
                    f"(integer), got `{got}`"
                )
            continue
        if name not in all_server_flags:
            continue
        truth = all_server_flags[name].get("default", "")
        got = sec.default or ""
        if not values_equivalent(got, truth):
            errors.append(f"--{name}: default `{got}` != server `{truth}`")
    return errors


# --- Reporting ---------------------------------------------------------------

def print_report(
    raw_count: int,
    user_count: int,
    excluded_examples: list[str],
    mech: MechResult,
    polish_changed_flags: list[str] | None,
    polish_validation_errors: list[str],
    polish_skipped_reason: str | None,
    polish_notes: list[str],
    dry_run: bool,
) -> int:
    print("")
    print("Ground truth:")
    print(f"  total server flags ({{--helpfull}}):  {raw_count}")
    print(f"  user-facing (Dragonfly):            {user_count}")
    excluded_n = raw_count - user_count
    sample = ", ".join(f"--{n}" for n in excluded_examples[:5])
    print(f"  upstream/library (excluded):        {excluded_n}"
          f" — e.g. {sample}{', ...' if len(excluded_examples) > 5 else ''}")
    print(f"  (these are glog/absl logging & arg-plumbing flags;")
    print(f"   they are statically linked but are not Dragonfly's documented surface)")

    print("")
    print("Mechanical pass:")
    print(f"  default values fixed:        {len(mech.fixed_defaults)}")
    print(f"  enum-typed deferred to LLM:  {len(mech.deferred_enum)}")
    print(f"  default-fix failures:        {len(mech.failed_defaults)}")
    print(f"  obsolete sections removed:   {len(mech.removed_from_doc)}")
    print(f"  flags missing from doc:      {len(mech.missing_from_doc)}")

    if mech.fixed_defaults:
        print("\n=== Defaults updated mechanically ===")
        for name, old, new in mech.fixed_defaults:
            print(f"  --{name}: `{old}` → `{new}`")

    if mech.deferred_enum:
        print("\n=== Enum-typed defaults deferred to LLM polish ===")
        print("  (kept as integer in `default:`; LLM expands description "
              "with the value table)")
        for name, doc, server in mech.deferred_enum:
            print(f"  --{name}: doc=`{doc}` server=`{server}`")

    if polish_skipped_reason:
        print(f"\nLLM polish: skipped ({polish_skipped_reason})")
    elif polish_validation_errors:
        print(f"\nLLM polish: VALIDATION FAILED — output discarded")
        for e in polish_validation_errors[:20]:
            print(f"  ✗ {e}")
        if len(polish_validation_errors) > 20:
            print(f"  ... ({len(polish_validation_errors) - 20} more)")
    else:
        print(f"\nLLM polish: applied")
        if polish_changed_flags:
            print(f"  refreshed {len(polish_changed_flags)} flag section(s)")
        for n in polish_notes[:10]:
            print(f"  note: {n}")

    failed = 0

    if mech.failed_defaults:
        failed = 1
        print(f"\n=== Default-fix FAILURES ({len(mech.failed_defaults)}) ===")
        for name, reason in mech.failed_defaults:
            print(f"  --{name}: {reason}")

    if mech.removed_from_doc:
        print(f"\n=== Removed obsolete flag sections "
              f"({len(mech.removed_from_doc)}) — server no longer reports these ===")
        for n in mech.removed_from_doc:
            print(f"  --{n}")

    if mech.missing_from_doc and (polish_skipped_reason or polish_validation_errors):
        failed = 1
        print(f"\n=== Flags missing from doc, NOT added "
              f"({len(mech.missing_from_doc)}) — re-run with LLM polish ===")
        for n in mech.missing_from_doc[:30]:
            print(f"  --{n}")
        if len(mech.missing_from_doc) > 30:
            print(f"  ... ({len(mech.missing_from_doc) - 30} more)")

    if dry_run:
        print("\n(dry-run — no files written)")
    return failed


# --- Main --------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--tag", help="Dragonfly tag (e.g. v1.38.0).")
    g.add_argument("--facts", type=Path,
                   help="Pre-captured facts JSON (skips Docker).")
    ap.add_argument("--skip-pull", action="store_true",
                    help="Skip docker pull when capturing facts.")
    ap.add_argument("--refresh-facts", action="store_true",
                    help="Re-capture facts even if cached.")
    ap.add_argument("--refresh-source", action="store_true",
                    help="Re-fetch & re-parse source even if cached.")
    ap.add_argument("--skip-source", action="store_true",
                    help="Skip C++ source parsing (LLM gets --helpfull only).")
    ap.add_argument("--dry-run", action="store_true",
                    help="Print everything without writing the page.")
    ap.add_argument("--no-llm", action="store_true",
                    help="Skip LLM polish step (mechanical pass only).")
    args = ap.parse_args()

    if args.facts and not args.skip_source:
        # We need a tag to fetch source. If --facts is used without --tag,
        # try to read tag from the facts file.
        try:
            facts_preview = json.loads(args.facts.read_text(encoding="utf-8"))
            args.tag = facts_preview.get("tag")
        except Exception:
            args.tag = None
        if not args.tag:
            print("warning: --facts without --tag and tag not in facts file; "
                  "skipping source capture")
            args.skip_source = True

    if not FLAGS_PAGE.exists():
        ap.error(f"flags page not found: {FLAGS_PAGE}")

    facts = load_facts(args)
    all_server_flags = facts["data"]["flags"]
    user_facing_flags = filter_user_facing(all_server_flags)
    excluded = sorted(set(all_server_flags) - set(user_facing_flags))

    page_text = FLAGS_PAGE.read_text(encoding="utf-8")
    mech_text, mech = mechanical_pass(page_text, all_server_flags, user_facing_flags)

    polish_skipped_reason: str | None = None
    polish_validation_errors: list[str] = []
    polish_changed_flags: list[str] | None = None
    polish_notes: list[str] = []
    final_text = mech_text

    will_run_llm = (
        not args.no_llm
        and bool(os.getenv("ANTHROPIC_API_KEY"))
        and (mech.missing_from_doc or mech.removed_from_doc
             or mech.fixed_defaults or mech.deferred_enum)
    )

    if args.no_llm:
        polish_skipped_reason = "--no-llm"
    elif not os.getenv("ANTHROPIC_API_KEY"):
        polish_skipped_reason = "ANTHROPIC_API_KEY not set"
    elif not (mech.missing_from_doc or mech.removed_from_doc
              or mech.fixed_defaults or mech.deferred_enum):
        polish_skipped_reason = "page already matches server, nothing to polish"

    source_facts: dict[str, dict] = {}
    if will_run_llm and not args.skip_source:
        target = set(all_server_flags.keys())
        try:
            source_facts = load_or_capture_source(args, target)
        except Exception as e:
            print(f"  warning: source capture failed ({e}); "
                  f"LLM will only have --helpfull data")
            source_facts = {}

    if will_run_llm:
        try:
            import anthropic
        except ImportError:
            polish_skipped_reason = "anthropic SDK not installed"
        else:
            print("\nCalling Claude for full-page polish...")
            client = anthropic.Anthropic()
            # Closed-world set: exactly the flags that should appear in the
            # output. Existing in the page (mechanically reconciled) plus
            # new user-facing ones to add. Upstream glog/absl flags that
            # aren't already in the doc are excluded by construction.
            must_be_present_set = (
                set(parse_sections(mech_text).keys()) | set(mech.missing_from_doc)
            )
            must_be_present = sorted(must_be_present_set)
            # Restrict ground_truth and source_facts to this set so the LLM
            # can't be tempted to add upstream flags it sees in the dict.
            gt_for_llm = {
                n: all_server_flags[n] for n in must_be_present_set
                if n in all_server_flags
            }
            sf_for_llm = {
                n: source_facts[n] for n in must_be_present_set
                if n in source_facts
            }
            enum_defaults_to_expand = [
                {"flag": n, "doc_default": doc, "server_default": server}
                for (n, doc, server) in mech.deferred_enum
            ]
            user_text = build_polish_user_text(
                mech_text, gt_for_llm, sf_for_llm, must_be_present,
                mech.missing_from_doc, enum_defaults_to_expand,
            )
            try:
                parsed, usage = call_llm(client, POLISH_SYSTEM, user_text)
            except Exception as e:
                polish_skipped_reason = f"LLM call failed: {e}"
            else:
                print(f"  tokens: in={usage['input_tokens']} "
                      f"out={usage['output_tokens']} stop={usage['stop_reason']}")
                polished = parsed.get("markdown", "")
                polish_notes = parsed.get("notes", []) or []
                if not polished.strip():
                    polish_validation_errors.append("LLM returned empty markdown")
                else:
                    polished, dropped = deduplicate_sections(polished)
                    if dropped:
                        polish_notes.append(
                            f"auto-deduped {len(dropped)} duplicate section(s): "
                            f"{sorted(set(dropped))}"
                        )
                    polished, repaired = repair_stub_sections(polished, mech_text)
                    if repaired:
                        polish_notes.append(
                            f"auto-repaired {len(repaired)} stub section(s) "
                            f"from input: {sorted(set(repaired))}"
                        )
                    polished, restored = restore_missing_sections(
                        polished, mech_text, must_be_present_set,
                    )
                    if restored:
                        polish_notes.append(
                            f"auto-restored {len(restored)} missing section(s) "
                            f"from input: {sorted(set(restored))}"
                        )
                    enum_keep_int = {n: doc for (n, doc, _) in mech.deferred_enum}
                    polish_validation_errors = validate_polish(
                        polished, all_server_flags, must_be_present_set, enum_keep_int,
                    )
                    if polish_validation_errors:
                        # Save raw output so the user can inspect it.
                        debug = SOURCE_DIR.parent / "llm_debug" / f"flags_polish_validation_failed_{datetime.now(timezone.utc):%Y%m%dT%H%M%SZ}.md"
                        debug.parent.mkdir(parents=True, exist_ok=True)
                        debug.write_text(polished, encoding="utf-8")
                        print(f"  raw LLM output saved to "
                              f"{debug.relative_to(REPO_ROOT)} for inspection")
                    if not polish_validation_errors:
                        final_text = polished
                        polish_changed_flags = sorted(
                            set(mech.missing_from_doc)
                            | {n for n, _, _ in mech.fixed_defaults}
                            | {n for n, _, _ in mech.deferred_enum}
                        )

    if not args.dry_run:
        FLAGS_PAGE.write_text(final_text, encoding="utf-8")

    return print_report(
        raw_count=len(all_server_flags),
        user_count=len(user_facing_flags),
        excluded_examples=excluded,
        mech=mech,
        polish_changed_flags=polish_changed_flags,
        polish_validation_errors=polish_validation_errors,
        polish_skipped_reason=polish_skipped_reason,
        polish_notes=polish_notes,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    sys.exit(main())
