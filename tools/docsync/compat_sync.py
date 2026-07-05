#!/usr/bin/env python3
"""compat_sync.py — rebuild docs/command-reference/compatibility.md deterministically.

Every support label is derived from source ground truth — the Redis command specs
and the Dragonfly source tree. No LLM, no runtime probing: the same checkouts always
produce the same table, and a new Redis/Dragonfly version is handled by re-reading the
sources. The label is SURFACE CAPABILITY (does Dragonfly accept the command/option),
never behaviour — output/ordering/error-text differences do not reduce it.

The curated table owns the row SET; only the labels are recomputed. The doc is written
only with --write-table; otherwise the run just emits artifacts under
tools/generated/compatibility/<ts>/. Docker is used only to detect module versions.
See tools/docsync/README.md for the label rules and architecture.

Usage:
    # Recompute labels + write draft/change-log (does NOT touch the doc):
    python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4

    # ...then apply the recomputed labels to compatibility.md:
    python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4 --write-table

    # Advisory model review of every row (flags disagreements, never changes a label;
    # needs OPENAI_API_KEY):
    python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4 --review

    # Pin a module version instead of the image-detected one:
    python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4 --module-ref search=v8.6.7

Artifacts: metadata.json (run config + module tag@sha), assessments.json (per-row
status/details/evidence), tasks.json (applied label changes, missing rows, unresolved
names), unsupported_commands.{json,md}, draft_table.md (== what --write-table writes).
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import html
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
COMPAT_PAGE = REPO_ROOT / "docs" / "command-reference" / "compatibility.md"
DOCS_COMMAND_DIR = REPO_ROOT / "docs" / "command-reference"
GENERATED = REPO_ROOT / "tools" / "generated"
COMPAT_GENERATED = GENERATED / "compatibility"

REDIS_REPO = "https://github.com/redis/redis.git"
REDIS_CHECKOUT = Path("/tmp/redis-docsync")
DRAGONFLY_REPO = "https://github.com/dragonflydb/dragonfly.git"
DRAGONFLY_CHECKOUT = Path("/tmp/dragonfly-docsync")
DRAGONFLY_IMAGE = "docker.dragonflydb.io/dragonflydb/dragonfly"

# Module command surfaces (options/tokens) live in each module repo's root
# commands.json, not in core Redis. Mandatory: without them all of Search/JSON/
# Bloom/… has no spec baseline. Version is auto-detected from the image's MODULE
# LIST, falling back to DEFAULT_MODULE_REFS below.
MODULE_SOURCES = {
    "search": ("https://github.com/RediSearch/RediSearch.git", Path("/tmp/redisearch-docsync")),
    "json": ("https://github.com/RedisJSON/RedisJSON.git", Path("/tmp/redisjson-docsync")),
    "bloom": ("https://github.com/RedisBloom/RedisBloom.git", Path("/tmp/redisbloom-docsync")),
    "timeseries": ("https://github.com/RedisTimeSeries/RedisTimeSeries.git", Path("/tmp/redistimeseries-docsync")),
}
# MODULE LIST reports these names; map them to our source keys.
MODULE_LIST_NAME_TO_KEY = {
    "search": "search", "searchlight": "search",
    "rejson": "json", "bf": "bloom", "timeseries": "timeseries",
}
# Fallback module refs when MODULE LIST cannot be read (no Docker). These are the
# versions bundled in redis:8.6.4 (from its MODULE LIST); update when the default
# --redis-ref moves. Auto-detection supersedes these whenever the image is up.
DEFAULT_MODULE_REFS = {
    "search": "v8.6.8",
    "json": "v8.6.0",
    "bloom": "v8.6.2",
    "timeseries": "v8.6.2",
}

PING_TIMEOUT_S = 30
DEFAULT_RETRIES = 10

H1_RE = re.compile(r"^#[ \t]+(?P<text>[^\n]+?)\s*$", re.MULTILINE)
REDIS_MODULE_FAMILIES = "BF, CF, CMS, FT, JSON, TDIGEST, TOPK, TS"

STATUS_LABELS = {
    "supported": "Fully supported",
    "partial": "Partially supported",
    "unsupported": "Unsupported",
    "dragonfly-specific": "Dragonfly-specific",
    "needs-review": "Needs review",
}

STATUS_CLASSES = {
    "supported": "supported",
    "partial": "partial",
    "unsupported": "unsupported",
    "dragonfly-specific": "dragonfly",
    "needs-review": "partial",
}

LABEL_TO_STATUS = {
    "fully supported": "supported",
    "fully Supported".lower(): "supported",
    "supported": "supported",
    "partially supported": "partial",
    "partial": "partial",
    "unsupported": "unsupported",
    "not supported": "unsupported",
    "dragonfly-specific": "dragonfly-specific",
    "dragonfly specific": "dragonfly-specific",
    "needs review": "needs-review",
}

PLACEHOLDER_COMMANDS = {"", "TBD", "NOT SUPPORTED"}

DIR_TO_FAMILY = {
    "acl": "Server",
    "bitmap": "Bitmap",
    "bloom-filter": "Bloom Filter",
    "cluster-management": "Cluster",
    "generic": "Generic",
    "geo": "Geo",
    "hashes": "Hash",
    "hyperloglog": "HyperLogLog",
    "json": "JSON",
    "list": "List",
    "pubsub": "PubSub",
    "rate-limiter": "Rate Limiter",
    "scripting": "Scripting",
    "search": "Search",
    "server-management": "Server",
    "sets": "Set",
    "sorted-sets": "Sorted Set",
    "stream": "Stream",
    "strings": "String",
    "transactions": "Transactions",
}

REDIS_GROUP_TO_FAMILY = {
    "bitmap": "Bitmap",
    "cluster": "Cluster",
    "connection": "Connection",
    "generic": "Generic",
    "geo": "Geo",
    "hash": "Hash",
    "hyperloglog": "HyperLogLog",
    "list": "List",
    "pubsub": "PubSub",
    "scripting": "Scripting",
    "server": "Server",
    "set": "Set",
    "sorted-set": "Sorted Set",
    "stream": "Stream",
    "string": "String",
    "transactions": "Transactions",
}

COMMAND_PREFIX_TO_FAMILY = {
    "ACL ": "Server",
    "BF.": "Bloom Filter",
    "BIT": "Bitmap",
    "CF.": "CF",
    "CLIENT ": "Connection",
    "CLUSTER ": "Cluster",
    "CMS.": "Count-Min Sketch",
    "COMMAND ": "Server",
    "CONFIG ": "Server",
    "EVAL": "Scripting",
    "FCALL": "Scripting",
    "FT.": "Search",
    "FUNCTION ": "Scripting",
    "GEO": "Geo",
    "H": "Hash",
    "JSON.": "JSON",
    "LATENCY ": "Server",
    "MEMORY ": "Server",
    "MODULE ": "Server",
    "PF": "HyperLogLog",
    "PUBSUB ": "PubSub",
    "SCRIPT ": "Scripting",
    "SLOWLOG ": "Server",
    "TOPK.": "Top-K",
    "TS.": "Time Series",
    "X": "Stream",
    "Z": "Sorted Set",
}

SOURCE_PATTERNS = ("*.cc", "*.h", "*.y", "*.yy", "*.ll", "*.l")
DRAGONFLY_REGISTERED_COMMAND_RE = re.compile(
    r'CI\{\s*"(?P<command>[^"]+)"'
)


def iter_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for pattern in SOURCE_PATTERNS:
        files.extend(root.rglob(pattern))
    return sorted(set(files))

@dataclass
class CompatRow:
    family: str
    command: str
    status: str
    details: str = ""
    line_no: int = 0
    source: str = "current"

    @property
    def key(self) -> str:
        return normalize_command(self.command)


@dataclass
class RedisCommandSpec:
    name: str
    group: str = ""
    arity: int | None = None
    function: str = ""
    tokens: list[str] = field(default_factory=list)
    arguments: list[dict[str, Any]] = field(default_factory=list)
    raw: dict[str, Any] = field(default_factory=dict)


@dataclass
class Assessment:
    row: CompatRow
    proposed_status: str
    unsupported_details: str
    confidence: str = "low"
    source: str = "deterministic"
    evidence: list[str] = field(default_factory=list)
    tasks: list[dict[str, Any]] = field(default_factory=list)
    # True when the source-derived verdict should replace the curated label
    # (False only for placeholders / names found in neither source).
    deterministic_change: bool = False
    # Optional independent model review of this row's deterministic verdict:
    # {"agree": bool, "concern": str, "suggested_status": str|None}. Advisory —
    # it never changes the label; disagreements become review-flag tasks.
    review: dict[str, Any] | None = None


@dataclass
class DockerSession:
    kind: str
    image: str
    container: str


def run(cmd: list[str], cwd: Path | None = None,
        check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=check)


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", s).strip("_") or "unknown"


def normalize_command(command: str) -> str:
    command = html.unescape(command)
    command = command.replace("\\*", "*")
    command = command.replace("|", " ")
    command = re.sub(r"<[^>]+>", "", command)
    command = re.sub(r"\s+", " ", command).strip()
    return command.upper()


def normalize_status(label: str) -> str:
    label = re.sub(r"<[^>]+>", "", label)
    label = html.unescape(label).strip().lower()
    label = re.sub(r"\s+", " ", label)
    return LABEL_TO_STATUS.get(label, label.replace(" ", "-"))


def strip_span(cell: str) -> str:
    text = re.sub(r"<[^>]+>", "", cell)
    return html.unescape(text).strip()


def split_markdown_row(line: str) -> list[str]:
    s = line.strip()
    if not s.startswith("|") or not s.endswith("|"):
        return []
    inner = s[1:-1]
    cells: list[str] = []
    cur: list[str] = []
    escaped = False
    for ch in inner:
        if ch == "\\" and not escaped:
            escaped = True
            cur.append(ch)
            continue
        if ch == "|" and not escaped:
            cells.append("".join(cur).strip())
            cur = []
            continue
        cur.append(ch)
        escaped = False
    cells.append("".join(cur).strip())
    return cells


def escape_markdown_cell(value: str) -> str:
    return value.replace("|", "\\|").strip()


def parse_compat_table(path: Path) -> tuple[str, list[CompatRow], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    header_idx = None
    for i, line in enumerate(lines):
        if "| Command Family" in line and "Dragonfly Support" in line:
            header_idx = i
            break
    if header_idx is None:
        raise RuntimeError(f"compatibility table header not found in {path}")

    end_idx = header_idx + 1
    while end_idx + 1 < len(lines) and lines[end_idx + 1].lstrip().startswith("|"):
        end_idx += 1

    before = "\n".join(lines[:header_idx])
    after = "\n".join(lines[end_idx + 1:])

    rows: list[CompatRow] = []
    current_family = ""
    for line_no, line in enumerate(lines[header_idx + 2:end_idx + 1], header_idx + 3):
        cells = split_markdown_row(line)
        if len(cells) < 3:
            continue
        family_cell, command_cell, support_cell = cells[:3]
        details_cell = cells[3] if len(cells) > 3 else ""
        family = strip_span(family_cell)
        if family:
            current_family = family
        command = strip_span(command_cell).replace("\\*", "*")
        status = normalize_status(strip_span(support_cell))
        rows.append(CompatRow(
            family=current_family,
            command=command,
            status=status,
            details=details_cell.strip(),
            line_no=line_no,
        ))

    return before, rows, after


def render_support(status: str) -> str:
    label = STATUS_LABELS.get(status, status.replace("-", " ").title())
    css = STATUS_CLASSES.get(status, status)
    return f'<span class="support {css}">{label}</span>'


def strip_generated_footer(after: str) -> str:
    lines = [
        line for line in after.splitlines()
        if not line.startswith("Verification:") and not line.lstrip().startswith("|")
    ]
    return "\n".join(lines).strip()


def verification_note(args: argparse.Namespace) -> str:
    dragonfly = args.dragonfly_ref or "selected Dragonfly build"
    redis = args.redis_ref or "selected Redis build"
    return f"Verification: Dragonfly {dragonfly}; Redis {redis}; modules: {REDIS_MODULE_FAMILIES}."


def docs_table_rows(rows: list[CompatRow]) -> list[CompatRow]:
    return rows


def unsupported_table_rows(rows: list[CompatRow]) -> list[CompatRow]:
    return [row for row in rows if row.status == "unsupported"]


def detail_for_docs(row: CompatRow) -> str:
    if row.status != "partial":
        return ""
    return re.sub(r"\s+", " ", row.details).strip()


def render_compat_table(before: str, rows: list[CompatRow], after: str,
                        footer: str = "") -> str:
    rendered: list[list[str]] = []
    previous_family = None
    for row in docs_table_rows(rows):
        family_cell = ""
        if row.family != previous_family:
            family_cell = f'<span class="family">{escape_markdown_cell(row.family)}</span>'
            previous_family = row.family
        command = escape_markdown_cell(row.command)
        rendered.append([
            family_cell,
            f'<span class="command">{command}</span>',
            render_support(row.status),
            escape_markdown_cell(detail_for_docs(row)),
        ])

    header = ["Command Family", "Command", "Dragonfly Support", "Details"]

    def fmt(cells: list[str]) -> str:
        return "| " + " | ".join(cells) + " |"

    table_lines = [fmt(header), "|:--|:--|:--|:--|"]
    table_lines.extend(fmt(cells) for cells in rendered)
    out = "\n".join([before.rstrip(), "", *table_lines])
    # Preserve any human-authored prose that lived below the table (notes,
    # legends, links). strip_generated_footer removes the old table rows and
    # the previous generated "Verification:" line so we do not duplicate them.
    tail = strip_generated_footer(after)
    if tail:
        out += "\n\n" + tail
    if footer:
        out += "\n\n" + footer
    return out.rstrip() + "\n"


def extract_h1(text: str) -> str | None:
    m = H1_RE.search(text)
    if not m:
        return None
    return normalize_command(m.group("text").strip().strip("`").strip())


def family_for_doc(path: Path) -> str:
    try:
        rel = path.relative_to(DOCS_COMMAND_DIR)
    except ValueError:
        return "Dragonfly"
    first = rel.parts[0] if rel.parts else ""
    return DIR_TO_FAMILY.get(first, first.replace("-", " ").title() or "Dragonfly")


def family_for_command(command: str, redis_spec: RedisCommandSpec | None = None) -> str:
    if redis_spec:
        return REDIS_GROUP_TO_FAMILY.get(
            redis_spec.group,
            redis_spec.group.replace("-", " ").title() or "Other",
        )
    key = normalize_command(command)
    for prefix, family in COMMAND_PREFIX_TO_FAMILY.items():
        if key.startswith(prefix):
            return family
    if key.startswith(("L", "R", "B")) and any(token in key for token in ("POP", "PUSH", "RANGE", "TRIM", "MOVE")):
        return "List"
    if key.startswith("S"):
        return "Set"
    return "Server"


def command_matches(command: str, available: set[str]) -> list[str]:
    key = normalize_command(command)
    if key in PLACEHOLDER_COMMANDS:
        return []
    if "*" in key:
        prefix = key.split("*", 1)[0].strip()
        return sorted(c for c in available if c.startswith(prefix))
    return [key] if key in available else []


# Internal/administrative commands that must never appear in the PUBLIC
# compatibility table: replication/cluster coordination, debug, and any
# underscore- or DFLY-prefixed handler.
INTERNAL_COMMAND_NAMES = {
    "DFLY", "DFLYCLUSTER", "DFLYMIGRATE", "ADDREPLICAOF", "REPLTAKEOVER",
}


def is_internal_command(command: str) -> bool:
    key = normalize_command(command)
    bare = key.split(" ", 1)[0]
    if bare in INTERNAL_COMMAND_NAMES or bare.startswith("DFLY"):
        return True
    # Underscore-prefixed or *_DEBUG / *_LIST / *_HELP internal handlers,
    # including module debug entries such as FT._DEBUG / FT._LIST.
    last = bare.rsplit(".", 1)[-1]
    if last.startswith("_"):
        return True
    return bare.endswith(("_DEBUG", "_LIST", "_HELP")) or "._" in bare


def is_cluster_command(command: str, family: str = "") -> bool:
    key = normalize_command(command)
    return family == "Cluster" or key.startswith("CLUSTER ") or key in {"ASKING", "READONLY", "READWRITE"}


def filter_rows(rows: list[CompatRow], patterns: list[str]) -> list[CompatRow]:
    if not patterns:
        return rows
    out = []
    for row in rows:
        key = row.key
        if any(fnmatch(key, p.upper()) or fnmatch(row.command, p) for p in patterns):
            out.append(row)
    return out


def progress(message: str) -> None:
    print(f"  {message}", flush=True)


def display_path(path: Path) -> str:
    """Repo-relative path when possible, else the path as given (e.g. a --output
    pointed outside the repo)."""
    try:
        return str(path.resolve().relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def should_report(index: int, total: int, every: int) -> bool:
    return index == 1 or index == total or (every > 0 and index % every == 0)


def ensure_checkout(name: str, repo: str, checkout: Path, ref: str, refresh: bool) -> Path:
    if not (checkout / ".git").exists():
        checkout.parent.mkdir(parents=True, exist_ok=True)
        print(f"  cloning {name} source to {checkout}...")
        run(["git", "clone", "--quiet", repo, str(checkout)])
    if refresh:
        run(["git", "fetch", "--tags", "--quiet"], cwd=checkout, check=False)
    # Discard any leftover local state so a reused checkout is byte-identical to a
    # fresh clone at `ref` — the determinism guarantee depends on a clean tree.
    run(["git", "reset", "--hard", "--quiet"], cwd=checkout, check=False)
    run(["git", "clean", "-fdxq"], cwd=checkout, check=False)
    run(["git", "checkout", "--quiet", ref], cwd=checkout)
    return checkout


def resolve_redis_source(args: argparse.Namespace) -> Path | None:
    if args.redis_source_dir:
        return args.redis_source_dir
    if not args.redis_ref:
        raise RuntimeError("--redis-ref (or --redis-source-dir) is required")
    return ensure_checkout("Redis", REDIS_REPO, REDIS_CHECKOUT, args.redis_ref, args.refresh_source)


def parse_module_refs(pairs: list[str]) -> dict[str, str]:
    """Parse repeated --module-ref name=ref into {name: ref}."""
    out: dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise RuntimeError(f"--module-ref expects name=ref, got {item!r}")
        name, ref = item.split("=", 1)
        key = name.strip().lower()
        if key not in MODULE_SOURCES:
            raise RuntimeError(f"unknown module {key!r}; expected one of {sorted(MODULE_SOURCES)}")
        out[key] = ref.strip()
    return out


def decode_module_version(ver: int) -> str:
    """Redis encodes module versions as major*10000 + minor*100 + patch; module
    repos tag them as vMAJOR.MINOR.PATCH."""
    return f"v{ver // 10000}.{(ver // 100) % 100}.{ver % 100}"


def parse_module_list(text: str) -> dict[str, int]:
    """Parse `redis-cli MODULE LIST` (flat name/ver stream) into {name: version}."""
    tokens = [t.strip().strip('"') for t in text.splitlines() if t.strip()]
    modules: dict[str, int] = {}
    current: str | None = None
    i = 0
    while i < len(tokens):
        if tokens[i] == "name" and i + 1 < len(tokens):
            current = tokens[i + 1].lower()
            i += 2
            continue
        if tokens[i] == "ver" and i + 1 < len(tokens) and current is not None:
            digits = re.sub(r"[^0-9-]", "", tokens[i + 1])
            if digits:
                modules[current] = int(digits)
            i += 2
            continue
        i += 1
    return modules


def detect_module_refs_from_image(image: str, skip_pull: bool, retries: int) -> dict[str, str]:
    """Auto-detect module version tags from the Redis image's MODULE LIST — the
    authoritative, drift-proof baseline (always matches the image under test)."""
    session = None
    try:
        session = boot_docker("module-probe", image, skip_pull=skip_pull, retries=retries)
        p = run(["docker", "exec", session.container, "redis-cli", "MODULE", "LIST"], check=False)
        versions = parse_module_list(p.stdout)
    finally:
        kill_docker(session)
    refs: dict[str, str] = {}
    for name, ver in versions.items():
        key = MODULE_LIST_NAME_TO_KEY.get(name)
        if key and ver > 1:  # ver==1 is a built-in (e.g. vectorset), no repo tag
            refs[key] = decode_module_version(ver)
    return refs


def resolve_module_refs(args: argparse.Namespace) -> dict[str, str]:
    """Resolve the ref for every module: MODULE LIST auto-detection (from the
    Redis image) supersedes the static default, and an explicit --module-ref
    supersedes both."""
    refs = dict(DEFAULT_MODULE_REFS)
    try:
        image = resolve_redis_image(args)
        detected = detect_module_refs_from_image(image, args.skip_pull, retries=3)
        if detected:
            refs.update(detected)
            progress("module versions detected from image MODULE LIST: "
                     + ", ".join(f"{k}={v}" for k, v in sorted(detected.items())))
    except Exception as e:  # noqa: BLE001 - fall back to the static default set
        progress(f"could not auto-detect module versions ({e}); using defaults "
                 + ", ".join(f"{k}={v}" for k, v in sorted(refs.items())))
    refs.update(parse_module_refs(args.module_ref))
    return refs


def resolve_module_sources(args: argparse.Namespace) -> dict[str, Path]:
    """Clone/checkout every Redis module repo at its resolved ref. Modules are
    MANDATORY: any failure aborts the run (raises) rather than silently dropping
    an 18%-of-the-table baseline."""
    refs = resolve_module_refs(args)
    resolved: dict[str, Path] = {}
    for key, (repo, checkout) in MODULE_SOURCES.items():
        ref = refs[key]
        resolved[key] = ensure_checkout(f"module:{key}", repo, checkout, ref, args.refresh_source)
    return resolved


def module_source_versions(module_dirs: dict[str, Path]) -> dict[str, str]:
    """Resolved ref + commit SHA per module, recorded so option appearance/
    removal is diffable across runs."""
    versions: dict[str, str] = {}
    for name, root in module_dirs.items():
        tag = run(["git", "describe", "--tags", "--always"], cwd=root, check=False)
        sha = run(["git", "rev-parse", "--short", "HEAD"], cwd=root, check=False)
        label = tag.stdout.strip() or "?"
        versions[name] = f"{label}@{sha.stdout.strip()}" if sha.returncode == 0 else label
    return versions


def resolve_dragonfly_source(args: argparse.Namespace) -> Path | None:
    if args.dragonfly_source_dir:
        return args.dragonfly_source_dir
    if not args.dragonfly_ref:
        raise RuntimeError("--dragonfly-ref (or --dragonfly-source-dir) is required")
    return ensure_checkout(
        "Dragonfly", DRAGONFLY_REPO, DRAGONFLY_CHECKOUT,
        args.dragonfly_ref, args.refresh_source,
    )


# A real option keyword: an all-caps word (letters/underscore), optionally
# hyphenated (LIB-NAME, MALLOC-STATS). Excludes spec-artifact "tokens" like a
# default annotation (MAX_TERMS=100), a glob (LOAD *), or an example id (S1, S2).
_OPTION_KEYWORD_RE = re.compile(r"^[A-Z][A-Z_]*(?:-[A-Z]+)*$")


def _is_option_keyword(token: str) -> bool:
    tok = token.strip().upper()
    if len(tok) < 2:
        return False
    if "=" in tok or "*" in tok or any(c.isspace() for c in tok):
        return False
    if re.match(r"^[A-Z]\d+$", tok):  # S1, S2 — example ids, not options
        return False
    return bool(_OPTION_KEYWORD_RE.match(tok))


def collect_tokens(arguments: list[dict] | None) -> list[str]:
    tokens: set[str] = set()
    if not arguments:
        return []
    for arg in arguments:
        token = arg.get("token")
        if isinstance(token, str) and _is_option_keyword(token):
            tokens.add(token.upper())
        nested = arg.get("arguments")
        if isinstance(nested, list):
            tokens.update(collect_tokens(nested))
    return sorted(tokens)


def ingest_command_specs(payload: dict, specs: dict[str, RedisCommandSpec]) -> None:
    """Parse a {name: spec} command-spec map (a core src/commands/*.json file OR
    a module commands.json) into RedisCommandSpec entries, keyed by normalized
    command name."""
    if not isinstance(payload, dict):
        return
    for name, spec in payload.items():
        if not isinstance(spec, dict):
            continue
        container = str(spec.get("container") or "").strip()
        full_name = f"{container} {name}" if container else name
        arguments = spec.get("arguments") if isinstance(spec.get("arguments"), list) else []
        key = normalize_command(full_name)
        specs[key] = RedisCommandSpec(
            name=key,
            group=str(spec.get("group") or ""),
            arity=spec.get("arity") if isinstance(spec.get("arity"), int) else None,
            function=str(spec.get("function") or ""),
            tokens=collect_tokens(arguments),
            arguments=arguments,
            raw=spec,
        )


def load_redis_specs_from_checkout(path: Path) -> dict[str, RedisCommandSpec]:
    specs: dict[str, RedisCommandSpec] = {}
    command_dir = path / "src" / "commands"
    if not command_dir.exists():
        raise RuntimeError(f"Redis command specs not found: {command_dir}")
    for spec_file in sorted(command_dir.rglob("*.json")):
        ingest_command_specs(json.loads(spec_file.read_text(encoding="utf-8")), specs)
    return specs


def find_module_commands_json(root: Path) -> Path | None:
    for candidate in [root / "commands.json", *sorted(root.glob("*/commands.json"))]:
        if candidate.exists():
            return candidate
    hits = [p for p in root.rglob("commands.json") if "deps" not in p.parts]
    return hits[0] if hits else None


def load_module_specs(module_dirs: dict[str, Path]) -> dict[str, RedisCommandSpec]:
    specs: dict[str, RedisCommandSpec] = {}
    for name, root in module_dirs.items():
        commands_json = find_module_commands_json(root)
        # Module specs are mandatory: a missing/unreadable one would silently
        # strip every command of that module of its Redis baseline (mislabeling
        # e.g. all FT.* as dragonfly-specific), so fail instead of skipping.
        if not commands_json:
            raise RuntimeError(f"module {name}: no commands.json under {root}")
        before = len(specs)
        try:
            ingest_command_specs(json.loads(commands_json.read_text(encoding="utf-8")), specs)
        except (OSError, json.JSONDecodeError) as e:
            raise RuntimeError(f"module {name}: failed to read {commands_json}: {e}") from e
        progress(f"module {name}: {len(specs) - before} command spec(s) from {commands_json.name}")
    return specs


def _find_matching(text: str, open_pos: int, open_ch: str = "{", close_ch: str = "}") -> int:
    """Index of the brace matching the one at open_pos, or -1. C/C++ aware:
    braces inside // and /* */ comments, "strings" and 'char' literals don't
    count (else an apostrophe truncates the capture). A ' between digits is a
    digit separator (100'000), not a char literal."""
    depth = 0
    i = open_pos
    n = len(text)
    state: str | None = None  # None | "line" | "block" | '"' | "'"
    while i < n:
        c = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if state == "line":
            if c == "\n":
                state = None
        elif state == "block":
            if c == "*" and nxt == "/":
                state = None
                i += 2
                continue
        elif state in ('"', "'"):
            if c == "\\":
                i += 2
                continue
            if c == state:
                state = None
        elif c == "/" and nxt == "/":
            state = "line"
            i += 2
            continue
        elif c == "/" and nxt == "*":
            state = "block"
            i += 2
            continue
        elif c in ('"', "'"):
            if c == "'" and i > 0 and text[i - 1].isdigit() and nxt.isdigit():
                i += 1  # digit separator (100'000), not a char literal
                continue
            state = c
        elif c == open_ch:
            depth += 1
        elif c == close_ch:
            depth -= 1
            if depth == 0:
                return i
        i += 1
    return -1


def _line_no(text: str, pos: int) -> int:
    return text[:pos].count("\n") + 1


def _truncate(text: str, max_chars: int) -> str:
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n/* ... truncated ... */"


# PascalCase calls that are replies/logging/casts, not option-parsing delegation.
_DELEGATE_STOPWORDS = frozenset({
    "If", "For", "While", "Switch", "Return", "Move", "String", "StrCat",
    "SendError", "SendOk", "SendLong", "SendDouble", "SendNull", "SendNullArray",
    "SendBulkString", "SendSimpleString", "SendStringArr", "SendVerbatimString",
    "StartArray", "StartCollection", "DCHECK", "CHECK", "LOG", "VLOG", "DVLOG",
})


def _find_definition_in_text(text: str, fn: str) -> tuple[int, int] | None:
    """(start, end) span of `fn`'s definition (params + opening brace), not a
    call, or None. A qualified `fn` (ScanOpts::TryFrom) matches the class exactly
    so a generic method name resolves to the right file."""
    if "::" in fn:
        qualifier, base = fn.rsplit("::", 1)
        prefix = re.escape(qualifier) + r"\s*::\s*"
    else:
        base, prefix = fn, r"(?:[A-Za-z_]\w*::)?"
    body_re = re.compile(
        r"(?:^|\n)[^\n;{}]*?\b" + prefix + re.escape(base)
        + r"\s*\([^{};]*\)\s*(?:const|noexcept)?\s*\{",
        re.DOTALL,
    )
    m = body_re.search(text)
    if not m:
        return None
    open_brace = text.find("{", m.end() - 1)
    if open_brace < 0:
        return None
    close = _find_matching(text, open_brace)
    if close <= open_brace:
        return None
    return m.start(), close + 1


def _delegate_callees(body: str, own: set[str]) -> list[str]:
    """PascalCase functions called in a handler body, first-seen order — the
    likely delegated impl (Sort -> SortGeneric). A qualified call is kept
    qualified (ScanOpts::TryFrom) so it resolves to the right file. Reply/log/cast
    helpers are filtered out."""
    seen: list[str] = []
    for m in re.finditer(
        r"\b([A-Z][A-Za-z0-9_]{2,}(?:\s*::\s*[A-Z][A-Za-z0-9_]{2,})*)\s*\(", body):
        name = re.sub(r"\s*", "", m.group(1))
        bare = name.rsplit("::", 1)[-1]
        if bare in _DELEGATE_STOPWORDS or name in own or name in seen:
            continue
        seen.append(name)
    return seen


# Handler registration in Dragonfly: CI{"NAME", ...}.HFUNC(Fn) (and variants).
_REG_WITH_HANDLER_RE = re.compile(
    r'CI\{\s*"(?P<cmd>[^"]+)"(?P<body>[^}]*)\}\s*\.\s*'
    r'(?:HFUNC|MFUNC|HFUNC2|SetHandler|SetAsyncHandler)\s*\(\s*&?(?P<fn>[A-Za-z_]\w*)',
    re.DOTALL,
)

# A C++ definition "<ret type> [Class::]Name(params) {"; the leading return type
# distinguishes it from a call. Indexes every definition for cross-file delegation.
_FN_DEF_RE = re.compile(
    r"\n[A-Za-z_][\w:<>,&*\s]*?[ \t*&](?:[A-Za-z_]\w*::)?"
    r"(?P<name>[A-Za-z_]\w*)\s*\([^{};]*\)\s*(?:const|noexcept)?\s*\{"
)

# A file-scope (column 0) `= "..."`/`= {...}` declaration, e.g.
# `const char* AND_OP_NAME = "AND";`. Dragonfly compares some option tokens via
# such constants, so the literal never appears inside a walked function body.
_FILE_SCOPE_STRLIT_RE = re.compile(r'^\w[^\n]*=\s*[{"][^\n]*$', re.MULTILINE)


def _family_hint(key: str) -> str:
    """Delegation hint: the family word, so TOPK.RESERVE maps to topk_family.cc
    (not the never-matching stem "topk.reserve")."""
    return key.split()[0].split(".")[0].lower()


def _token_honored(token: str, text: str) -> bool:
    """Whether a Redis option/subcommand keyword is PARSED AND HONORED in `text`.
    Tested as a string LITERAL ("TOKEN") — the way Dragonfly matches options
    (parser.Check("X"), sub_cmd == "X"); a bare word matched variables (db_index
    for DB). Not honored if named only inside a rejection ("... not supported"):
    recognized but stubbed. Punctuation-only tokens (~, =) count as honored."""
    tok = token.strip().upper()
    if len(tok) < 2 or not re.search(r"[A-Z]", tok):
        return True
    if not re.search(r'"' + re.escape(tok) + r'"', text, re.IGNORECASE):
        return False
    rejected = re.search(
        r'"[^"]*\b' + re.escape(tok) + r'\b[^"]*(?:not supported|not implemented)"',
        text, re.IGNORECASE)
    return not rejected


# A dispatch branch whose ENTIRE body is a bare reply (return ...SendOk/
# SendEmptyArray/SendNull...): the subcommand is recognized but does no real work
# (LATENCY HISTOGRAM -> SendEmptyArray, FUNCTION FLUSH -> SendOk). Delegation to a
# worker (return Foo(...)) does not match, so real subcommands are untouched.
_STUB_REPLY_RE = re.compile(
    r'^\s*\{?\s*return\s+[^;{}]*?\bSend(?:Ok|EmptyArray|Empty|Null|NullArray|'
    r'SimpleString)\w*\s*\([^;{}]*\)\s*;\s*\}?\s*$')


def _is_stub_subcommand(token: str, text: str) -> bool:
    """True if `token` is dispatched (== "TOKEN") to a branch that only replies
    OK/empty and does nothing — a no-op stub, accepted but not truly supported."""
    tok = token.strip().upper()
    for m in re.finditer(r'==\s*"' + re.escape(tok) + r'"', text, re.IGNORECASE):
        j = text.find(")", m.end())  # close of the if-condition
        if j < 0:
            continue
        k = j + 1
        while k < len(text) and text[k] in " \t\n":
            k += 1
        if k < len(text) and text[k] == "{":
            close = _find_matching(text, k)
            branch = text[k:close + 1] if close > k else ""
        else:
            end = text.find(";", k)
            branch = text[k:end + 1] if end > k else ""
        if branch and _STUB_REPLY_RE.match(branch):
            return True
    return False


class DragonflySource:
    """Deterministic view of the Dragonfly source checkout.

    Scans every registration ONCE to build a command -> (file, handler) map and
    the set of registered commands, then answers, per command, the full
    implementation text (following delegation so options parsed in helpers or
    sibling files are visible) and which Redis option tokens are absent from it.
    This is the ground truth for the support label — no LLM, no runtime.
    """

    def __init__(self, root: Path | None):
        self.root = root
        self.src = (root / "src") if root else None
        all_files = (
            iter_source_files(self.src) if self.src and self.src.exists() else []
        )
        # Exclude test files: their fixtures/assertions leak option tokens.
        self._files: list[Path] = [p for p in all_files if "_test" not in p.name]
        self._text: dict[Path, str] = {}
        self._dir_blob: dict[Path, str] = {}
        self._filelits: dict[Path, str] = {}
        self._impl: dict[str, str] = {}
        self._handler_impl_cache: dict[str, str] = {}
        self.registered: set[str] = set()
        self.handler: dict[str, tuple[Path, str]] = {}
        self._fn_files: dict[str, list[Path]] = {}
        self._build_registry()

    def _files_defining(self, fn: str) -> list[Path]:
        return self._fn_files.get(fn, [])

    def _read(self, path: Path) -> str:
        if path not in self._text:
            try:
                self._text[path] = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                self._text[path] = ""
        return self._text[path]

    def _build_registry(self) -> None:
        for path in self._files:
            text = self._read(path)
            for m in DRAGONFLY_REGISTERED_COMMAND_RE.finditer(text):
                end = text.find("<<", m.end())
                reg = text[m.start():end if end != -1 else m.end() + 300]
                if "HIDDEN" in reg:
                    continue
                self.registered.add(normalize_command(m.group("command")))
            for m in _REG_WITH_HANDLER_RE.finditer(text):
                key = normalize_command(m.group("cmd"))
                if "HIDDEN" in m.group("body"):
                    continue
                self.handler.setdefault(key, (path, m.group("fn")))
            for m in _FN_DEF_RE.finditer(text):
                self._fn_files.setdefault(m.group("name"), [])
                if path not in self._fn_files[m.group("name")]:
                    self._fn_files[m.group("name")].append(path)

    def _dir_text(self, directory: Path) -> str:
        if directory not in self._dir_blob:
            self._dir_blob[directory] = "\n".join(
                self._read(p) for p in self._files if p.parent == directory
            )
        return self._dir_blob[directory]

    def _file_scope_literals(self, path: Path) -> str:
        if path not in self._filelits:
            self._filelits[path] = "\n".join(
                _FILE_SCOPE_STRLIT_RE.findall(self._read(path)))
        return self._filelits[path]

    def _delegation_text(self, path: Path, fn: str, hint: str = "",
                         budget: int = 60000, max_depth: int = 5) -> str:
        """Handler body + the bodies of functions it delegates to, across files,
        so options parsed in a helper or a *_mgr.cc/*_cmd.cc are captured. `hint`
        (the family word) disambiguates common callee names by file stem."""
        def rank(candidate: Path) -> tuple[int, int]:
            stem = candidate.stem.lower()
            return (0 if hint and hint in stem else 1, len(stem))

        pieces: list[str] = []
        visited: set[str] = set()
        total = 0
        queue: list[tuple[str, Path, int]] = [(f"Cmd{fn}", path, 0), (fn, path, 0)]
        while queue and total < budget:
            name, home, depth = queue.pop(0)
            if name in visited or depth > max_depth:
                continue
            visited.add(name)
            if _find_definition_in_text(self._read(home), name) is not None:
                # Defined here → the definition in scope; don't pull a same-named
                # def from another family (OpSet is in both hset_/json_family).
                candidates = [home]
            elif "::" in name:
                # Qualified (ScanOpts::TryFrom): the class pins the file, so a
                # precise match anywhere is safe — scan all, rank can't hide it.
                candidates = sorted(self._files_defining(name.rsplit("::", 1)[-1]),
                                    key=rank)
            elif hint:
                # Generic name (Parse/Run/Reserve): only follow it into a file of
                # the same family (stem carries the hint), else it drags in an
                # unrelated family's code.
                candidates = sorted(
                    (p for p in self._files_defining(name) if hint in p.stem.lower()),
                    key=rank)[:2]
            else:
                candidates = sorted(self._files_defining(name), key=rank)[:2]
            for cand in candidates:
                span = _find_definition_in_text(self._read(cand), name)
                if not span:
                    continue
                body = self._read(cand)[span[0]:span[1]]
                pieces.append(body)
                total += len(body)
                if depth < max_depth:
                    for callee in _delegate_callees(body, visited):
                        if callee not in visited:
                            queue.append((callee, cand, depth + 1))
                break
        return "\n".join(pieces)

    def _reg_for(self, command: str) -> tuple[Path, str] | None:
        key = normalize_command(command)
        reg = self.handler.get(key)
        if not reg:
            parts = key.split()
            if len(parts) > 1:
                reg = self.handler.get(parts[0])
        return reg

    def handler_impl(self, command: str) -> str:
        """Code reachable from THIS command's own handler (delegation-followed).
        Used for subcommand existence + the review excerpt: it excludes sibling
        handlers, so public CLUSTER doesn't reach internal DFLYCLUSTER FLUSHSLOTS."""
        key = normalize_command(command)
        cached = self._handler_impl_cache.get(key)
        if cached is not None:
            return cached
        reg = self._reg_for(command)
        text = self._delegation_text(reg[0], reg[1], hint=_family_hint(key)) if reg else ""
        self._handler_impl_cache[key] = text
        return text

    def implementation(self, command: str) -> str:
        """Dragonfly source implementing `command`, for OPTION presence. Module
        subdir commands (search/, acl/, cluster/) return the whole directory —
        their parsing is spread across sibling files; others return the handler +
        its delegated functions."""
        key = normalize_command(command)
        if key in self._impl:
            return self._impl[key]
        reg = self._reg_for(command)
        text = ""
        if reg:
            path, fn = reg
            if path.parent.name != "server":
                text = self._dir_text(path.parent)
            else:
                # + file-scope constants: some option tokens are compared via
                # `const char* X = "AND"`, never appearing in a walked body.
                text = (self._delegation_text(path, fn, hint=_family_hint(key))
                        + "\n" + self._file_scope_literals(path))
        self._impl[key] = text
        return text

    def command_exists(self, command: str) -> bool:
        key = normalize_command(command)
        if key in self.registered:
            return True
        parts = key.split()
        if len(parts) > 1 and parts[0] in self.registered:
            # Subcommand (CONFIG GET): exists iff the parent's own handler parses
            # and honors the token — and does real work, not a no-op reply stub
            # (LATENCY HISTOGRAM -> SendEmptyArray, FUNCTION FLUSH -> SendOk).
            impl = self.handler_impl(parts[0])
            return _token_honored(parts[1], impl) and not _is_stub_subcommand(parts[1], impl)
        return False

    def missing_options(self, command: str, spec: RedisCommandSpec | None) -> list[str]:
        if not spec or not spec.tokens:
            return []
        impl = self.implementation(command)
        if not impl:
            return []
        return sorted({t.strip().upper() for t in spec.tokens
                       if not _token_honored(t, impl)})


def insert_new_rows(rows: list[CompatRow], additions: list[CompatRow]) -> list[CompatRow]:
    """Merge `additions` into `rows`, keeping each family's rows contiguous: an
    addition is placed after the last existing row of its family, or appended as a
    new family group if that family is not present yet (the renderer emits the
    family name only when it changes, so families must stay grouped)."""
    merged = list(rows)
    for add in additions:
        last = max((i for i, r in enumerate(merged) if r.family == add.family),
                   default=None)
        if last is None:
            merged.append(add)
        else:
            merged.insert(last + 1, add)
    return merged


def add_missing_redis_rows(
    rows: list[CompatRow],
    redis_specs: dict[str, RedisCommandSpec],
) -> list[CompatRow]:
    existing = {row.key for row in rows}
    additions: list[CompatRow] = []
    for command, spec in sorted(redis_specs.items()):
        if command in existing or command in PLACEHOLDER_COMMANDS or is_internal_command(command):
            continue
        family = REDIS_GROUP_TO_FAMILY.get(spec.group, spec.group.replace("-", " ").title() or "Other")
        additions.append(CompatRow(
            family=family,
            command=command,
            status="needs-review",
            details="",
            source="redis-spec",
        ))
    if additions:
        progress(f"adding Redis spec rows missing from current table: {len(additions)}")
    return insert_new_rows(rows, additions)


def add_missing_dragonfly_rows(
    rows: list[CompatRow],
    dragonfly_commands: set[str],
    redis_specs: dict[str, RedisCommandSpec],
) -> list[CompatRow]:
    existing = {row.key for row in rows}
    additions: list[CompatRow] = []
    for command in sorted(dragonfly_commands):
        if command in existing or command in PLACEHOLDER_COMMANDS or is_internal_command(command):
            continue
        redis_spec = redis_specs.get(command)
        additions.append(CompatRow(
            family=family_for_command(command, redis_spec),
            command=command,
            status="needs-review",
            details="",
            source="dragonfly-source",
        ))
    if additions:
        progress(f"adding Dragonfly registered rows missing from current table: {len(additions)}")
    return insert_new_rows(rows, additions)


def missing_command_tasks(
    all_rows: list[CompatRow],
    redis_specs: dict[str, RedisCommandSpec],
    dragonfly_source_commands: set[str],
) -> list[dict[str, Any]]:
    """Report commands present in Redis/Dragonfly but absent from the curated
    table as tasks for a human, instead of auto-injecting rows. Internal/hidden
    commands are never reported."""
    existing = {row.key for row in all_rows}
    tasks: list[dict[str, Any]] = []
    seen: set[str] = set()

    def add(command: str, source: str) -> None:
        if (command in existing or command in PLACEHOLDER_COMMANDS
                or is_internal_command(command) or command in seen):
            return
        seen.add(command)
        tasks.append({
            "type": "missing-row",
            "source": source,
            "command": command,
            "message": "Command exists but is absent from the curated table; "
                       "add it manually if it should be tracked.",
        })

    for command in sorted(redis_specs):
        add(command, "redis-spec")
    for command in sorted(dragonfly_source_commands):
        add(command, "dragonfly-source")
    return tasks


def docker_pull(image: str, skip_pull: bool, retries: int) -> None:
    if skip_pull:
        return
    progress(f"pulling {image}...")
    last = None
    for attempt in range(1, retries + 1):
        last = run(["docker", "pull", image], check=False)
        if last.returncode == 0:
            return
        progress(
            f"docker pull attempt {attempt}/{retries} failed for {image}: "
            f"{(last.stderr or last.stdout).strip()}"
        )
        if attempt < retries:
            time.sleep(min(2 ** (attempt - 1), 10))
    raise RuntimeError(f"docker pull failed after {retries} attempt(s) for {image}: {last.stderr if last else ''}")


def boot_docker(kind: str, image: str,
                skip_pull: bool = False, retries: int = DEFAULT_RETRIES) -> DockerSession:
    docker_pull(image, skip_pull, retries)
    container = f"compat-{kind}-{slug(image)}-{os.getpid()}"
    run(["docker", "run", "-d", "--name", container, image])
    deadline = time.time() + PING_TIMEOUT_S
    while time.time() < deadline:
        p = run(["docker", "exec", container, "redis-cli", "PING"], check=False)
        if p.returncode == 0 and "PONG" in p.stdout:
            return DockerSession(kind=kind, image=image, container=container)
        time.sleep(0.3)
    subprocess.run(["docker", "rm", "-f", container], capture_output=True)
    raise RuntimeError(f"{kind} container {image} did not respond to PING")


def kill_docker(session: DockerSession | None) -> None:
    if session:
        subprocess.run(["docker", "rm", "-f", session.container], capture_output=True)


def deterministic_assessment(
    row: CompatRow,
    spec: RedisCommandSpec | None,
    df: DragonflySource,
) -> Assessment:
    """Derive the support label from source: (a) whether Dragonfly registers the
    command and (b) which of its Redis option tokens appear in the Dragonfly
    implementation. supported / partial / unsupported / dragonfly-specific."""
    if row.key in PLACEHOLDER_COMMANDS or "*" in row.command:
        # Placeholder (TBD) or wildcard shorthand (FUNCTION *): not a concrete
        # command whose subcommands can be assessed individually — keep curated
        # and flag rather than mark it supported off a punctuation "subcommand".
        return Assessment(
            row=row, proposed_status=row.status, unsupported_details=row.details,
            confidence="low", source="deterministic",
            evidence=["curated placeholder / wildcard row; no command-level assessment"],
            tasks=[{
                "type": "placeholder-row", "command": row.command, "family": row.family,
                "message": "Curated placeholder/wildcard row kept; decide whether per-subcommand rows are needed.",
            }],
        )

    in_dragonfly = df.command_exists(row.command)
    in_redis = spec is not None
    evidence = [
        f"Dragonfly source: {'registered' if in_dragonfly else 'not registered'}",
        f"Redis spec: {'present' if in_redis else 'absent'}",
    ]
    tasks: list[dict[str, Any]] = []
    details = ""

    if not in_dragonfly and not in_redis:
        # Neither source knows this command (e.g. a corrupted curated row name):
        # keep the curated label and flag it rather than guess.
        tasks.append({
            "type": "unresolved-command", "command": row.command, "family": row.family,
            "message": "Command not found in Redis specs or Dragonfly source; verify the row name.",
        })
        return Assessment(
            row=row, proposed_status=row.status, unsupported_details=row.details,
            confidence="low", source="deterministic", evidence=evidence,
            tasks=tasks, deterministic_change=False)

    if not in_dragonfly:
        status = "unsupported"
    elif not in_redis:
        status = "dragonfly-specific"
    else:
        missing = df.missing_options(row.command, spec)
        if missing:
            status = "partial"
            details = "Missing: " + ", ".join(missing) + "."
            evidence.append("Options absent from Dragonfly source: " + ", ".join(missing))
        else:
            status = "supported"

    if status != row.status:
        tasks.append({
            "type": "status-change", "command": row.command, "family": row.family,
            "from": row.status, "to": status,
        })

    return Assessment(
        row=row, proposed_status=status, unsupported_details=details,
        confidence="high", source="deterministic", evidence=evidence,
        tasks=tasks, deterministic_change=True)


def build_assessments(
    rows: list[CompatRow],
    redis_specs: dict[str, RedisCommandSpec],
    df: DragonflySource,
    progress_every: int,
) -> list[Assessment]:
    total = len(rows)
    assessments: list[Assessment] = []
    for index, row in enumerate(rows, 1):
        matches = command_matches(row.command, set(redis_specs))
        spec = redis_specs.get(matches[0]) if matches else None
        assessments.append(deterministic_assessment(row, spec, df))
        if should_report(index, total, progress_every):
            progress(f"assessment {index}/{total}: {row.family} / {row.command} -> {assessments[-1].proposed_status}")
    return assessments


# --- Model review layer (--review) --------------------------------------------
# Advisory only: the model reviews every deterministic verdict and flags concerns
# for a human (recognized-but-stubbed subcommands, a core option wrongly Missing,
# spec-artifact noise). It NEVER changes the shipped label.

REVIEW_SYSTEM = """\
You REVIEW a Dragonfly-vs-Redis compatibility verdict that was derived
deterministically from source code. You do NOT decide the label — you check the
automated verdict and flag concerns for a human.

You are given, per command: the automated status (supported / partial /
unsupported / dragonfly-specific), its "Missing:" option list (for partial), the
Redis option tokens from the command spec, and an excerpt of the Dragonfly
implementation source.

The support label is SURFACE CAPABILITY: whether Dragonfly accepts the command
and each Redis option. Output/value differences, ordering, precision, bugs,
intentional behavior changes, and error-response differences NEVER reduce
support (e.g. FT.INFO returning fewer fields is still Fully supported).

Flag a concern (agree=false) only for a concrete problem, such as:
  - WRONG STATUS: the excerpt shows the command is recognized but explicitly
    stubbed/not-implemented (should be unsupported, not supported); or a command
    marked unsupported that the excerpt clearly implements.
  - FALSE MISSING: a listed Missing option that is a fundamental/core part of the
    command (e.g. BITOP AND), or is clearly parsed in the excerpt under another
    spelling.
  - NOISE: "Missing" entries that are not real command options (aggregation
    function names, spec artifacts like S1, MAX_TERMS=100, "LOAD *").
  - FALSE SUPPORTED: a spec option that is genuinely absent but not listed.

Use your Redis/Dragonfly knowledge plus the provided evidence. Do NOT nitpick
wording or restate the label. Prefer agree=true unless you have a specific,
grounded reason.

Output JSON only:
{"agree": true|false, "concern": "" or "one specific issue",
 "suggested_status": null or "supported|partial|unsupported|dragonfly-specific"}
"""


def _call_openai_json(system: str, user: str, model: str, retries: int = 3) -> dict:
    try:
        from openai import OpenAI
    except ImportError as e:
        raise RuntimeError("openai SDK not installed (pip install openai)") from e
    client = OpenAI()
    last = None
    for attempt in range(1, retries + 1):
        try:
            resp = client.chat.completions.create(
                model=model, temperature=0, seed=7,
                messages=[{"role": "system", "content": system},
                          {"role": "user", "content": user}],
                response_format={"type": "json_object"},
            )
            return json.loads(resp.choices[0].message.content or "{}")
        except Exception as e:  # noqa: BLE001
            last = e
    raise RuntimeError(f"model review call failed after {retries} attempts: {last}")


def build_review_prompt(assessment: Assessment, spec: RedisCommandSpec | None,
                        impl_text: str) -> str:
    row = assessment.row
    payload = {
        "command": row.command,
        "family": row.family,
        "automated_status": assessment.proposed_status,
        "automated_missing_options": (
            [t.strip() for t in assessment.unsupported_details.replace("Missing:", "").rstrip(".").split(",") if t.strip()]
            if assessment.proposed_status == "partial" else []
        ),
        "redis_option_tokens": (spec.tokens if spec else []),
        "dragonfly_implementation_excerpt": _truncate(impl_text, 12000),
        "task": "Review the automated verdict. Flag a concrete problem or agree.",
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def review_assessments(
    assessments: list[Assessment],
    redis_specs: dict[str, RedisCommandSpec],
    df: DragonflySource,
    model: str,
    workers: int,
    progress_every: int,
) -> list[dict[str, Any]]:
    """Independently review every row's deterministic verdict with the model.
    Attaches assessment.review and returns review-flag tasks for disagreements.
    Never changes a label."""
    total = len(assessments)
    progress(f"model review of {total} row(s) using {model}")

    def review_one(a: Assessment) -> dict[str, Any]:
        matches = command_matches(a.row.command, set(redis_specs))
        spec = redis_specs.get(matches[0]) if matches else None
        # Command-specific handler code, not the whole-dir blob.
        impl = df.handler_impl(a.row.command)
        try:
            parsed = _call_openai_json(REVIEW_SYSTEM, build_review_prompt(a, spec, impl), model)
        except RuntimeError as e:
            return {"agree": True, "concern": "", "suggested_status": None, "error": str(e)}
        return {
            "agree": bool(parsed.get("agree", True)),
            "concern": str(parsed.get("concern") or "").strip(),
            "suggested_status": (normalize_status(str(parsed["suggested_status"]))
                                 if parsed.get("suggested_status") else None),
        }

    flags: list[dict[str, Any]] = []
    by_key = {(a.row.family, a.row.key): a for a in assessments}
    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        futures = {pool.submit(review_one, a): a for a in assessments}
        for done, fut in enumerate(as_completed(futures), 1):
            a = futures[fut]
            by_key[(a.row.family, a.row.key)].review = fut.result()
            if should_report(done, total, progress_every):
                progress(f"review {done}/{total}")
    for a in assessments:
        rev = a.review or {}
        if not rev.get("agree", True) and rev.get("concern"):
            flags.append({
                "type": "review-flag", "command": a.row.command, "family": a.row.family,
                "status": a.proposed_status, "suggested_status": rev.get("suggested_status"),
                "message": rev["concern"],
            })
    progress(f"model review complete: {len(flags)} row(s) flagged for human review")
    return flags


def serialize_dataclass(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: serialize_dataclass(v) for k, v in asdict(obj).items()}
    if isinstance(obj, list):
        return [serialize_dataclass(v) for v in obj]
    if isinstance(obj, dict):
        return {k: serialize_dataclass(v) for k, v in obj.items()}
    return obj


def assessments_to_rows(
    rows: list[CompatRow], assessments: list[Assessment]
) -> tuple[list[CompatRow], list[dict[str, Any]]]:
    """Apply deterministic verdicts to the curated rows.

    The source-derived verdict is authoritative, so it replaces the curated
    label/details; a row keeps its curated value only when the assessment could
    not resolve it (deterministic_change False — e.g. a placeholder or a name
    found in neither source). Every change from the curated label is recorded in
    the change log. Matching is by (family, command) so identical command names
    in different families do not collide.
    """
    by_key = {(a.row.family, a.row.key): a for a in assessments}
    out: list[CompatRow] = []
    change_log: list[dict[str, Any]] = []
    for row in rows:
        a = by_key.get((row.family, row.key))
        if not a or not a.deterministic_change:
            out.append(row)
            continue
        out.append(CompatRow(row.family, row.command, a.proposed_status,
                             a.unsupported_details, row.line_no, a.source))
        if a.proposed_status != row.status or a.unsupported_details != row.details:
            change_log.append({
                "type": "status-change-applied", "command": row.command, "family": row.family,
                "from": row.status, "to": a.proposed_status,
                "details": a.unsupported_details,
                "message": "Applied from deterministic source analysis.",
            })
    return out, change_log


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_unsupported_markdown(path: Path, rows: list[CompatRow]) -> None:
    lines = ["# Unsupported Commands", ""]
    if not rows:
        lines.append("No unsupported commands were identified.")
    else:
        current_family = ""
        for row in rows:
            if row.family != current_family:
                current_family = row.family
                lines.extend(["", f"## {current_family}"])
            lines.append(f"- `{row.command}`")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def write_artifacts(
    out_dir: Path,
    before: str,
    after: str,
    rows: list[CompatRow],
    assessments: list[Assessment],
    args: argparse.Namespace,
    draft_rows: list[CompatRow],
    change_log: list[dict[str, Any]],
    extra_tasks: list[dict[str, Any]] | None = None,
    module_versions: dict[str, str] | None = None,
) -> None:
    # draft_rows is the deterministic table computed once in main(), so the
    # preview a reviewer reads is byte-identical to what ships.
    out_dir.mkdir(parents=True, exist_ok=True)
    metadata = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "method": "deterministic source analysis (no LLM, no runtime)",
        "dragonfly_ref": args.dragonfly_ref,
        "redis_ref": args.redis_ref,
        "module_versions": module_versions or {},
        "row_count": len(rows),
    }
    write_json(out_dir / "metadata.json", metadata)
    write_json(out_dir / "assessments.json", serialize_dataclass(assessments))
    tasks = [task for assessment in assessments for task in assessment.tasks]
    tasks.extend(change_log)
    tasks.extend(extra_tasks or [])
    write_json(out_dir / "tasks.json", {"tasks": tasks})
    unsupported_rows = unsupported_table_rows(draft_rows)
    write_json(out_dir / "unsupported_commands.json", serialize_dataclass(unsupported_rows))
    write_unsupported_markdown(out_dir / "unsupported_commands.md", unsupported_rows)
    (out_dir / "draft_table.md").write_text(
        render_compat_table(before, draft_rows, after, verification_note(args)),
        encoding="utf-8",
    )


def print_summary(
    assessments: list[Assessment],
    out_dir: Path,
    write_table: bool,
    extra_tasks: list[dict[str, Any]] | None = None,
    review_flags: list[dict[str, Any]] | None = None,
) -> int:
    counts: dict[str, int] = {}
    tasks: list[dict[str, Any]] = []
    for assessment in assessments:
        counts[assessment.proposed_status] = counts.get(assessment.proposed_status, 0) + 1
        tasks.extend(assessment.tasks)
    tasks.extend(extra_tasks or [])

    review_types = {"unresolved-command", "placeholder-row"}
    review_tasks = [t for t in tasks if t.get("type") in review_types]
    print("")
    print("Support summary:")
    for status in ("supported", "partial", "unsupported", "dragonfly-specific"):
        if counts.get(status):
            print(f"  {STATUS_LABELS[status]}: {counts[status]}")
    if write_table:
        print("  Review diff: docs/command-reference/compatibility.md")
    else:
        print(f"  Review draft: {out_dir.relative_to(REPO_ROOT)}/draft_table.md")
    print(f"  Evidence artifacts: {out_dir.relative_to(REPO_ROOT)}")

    if review_tasks:
        print("")
        print("Rows the source analysis could not resolve (kept curated, verify by hand):")
        for task in review_tasks:
            print(f"  {task.get('family')} / {task.get('command')}: {task.get('message')}")
    if review_flags:
        print("")
        print(f"Model review flagged {len(review_flags)} row(s) — label unchanged, verify these:")
        for f in review_flags:
            sug = f" (suggests {f['suggested_status']})" if f.get("suggested_status") else ""
            print(f"  {f.get('family')} / {f.get('command')} [{f.get('status')}]{sug}: {f.get('message')}")
    return 0


def resolve_redis_image(args: argparse.Namespace) -> str:
    if args.redis_image:
        return args.redis_image
    if not args.redis_ref:
        raise RuntimeError("--redis-ref or --redis-image is required to detect module versions")
    return f"redis:{args.redis_ref}"


def add_cli_args() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dragonfly-ref",
                    help="Dragonfly tag/revision to check out and record (e.g. v1.39.0).")
    ap.add_argument("--dragonfly-source-dir", type=Path,
                    help="Existing Dragonfly source checkout. Skips cloning Dragonfly.")
    ap.add_argument("--redis-ref",
                    help="Redis git ref/tag; also the default Docker tag for module detection.")
    ap.add_argument("--redis-image",
                    help="Redis Docker image for MODULE LIST version detection. Defaults to redis:<redis-ref>.")
    ap.add_argument("--redis-source-dir", type=Path,
                    help="Existing Redis source checkout. Skips cloning Redis.")
    ap.add_argument("--input", type=Path, default=COMPAT_PAGE,
                    help="Compatibility markdown page to read.")
    ap.add_argument("--output", type=Path, default=COMPAT_PAGE,
                    help="Compatibility markdown page to write only when --write-table is set.")
    ap.add_argument("--filter", action="append", default=[],
                    help="Command glob filter, e.g. --filter 'FT.*'. Repeatable.")
    ap.add_argument("--limit", type=int, default=0,
                    help="Limit rows processed after filtering.")
    ap.add_argument("--module-ref", action="append", default=[], metavar="NAME=REF",
                    help="Override a module source ref, e.g. --module-ref search=v8.6.8. "
                         "Names: search, json, bloom, timeseries. By default the version is "
                         "auto-detected from the Redis image's MODULE LIST. Repeatable.")
    ap.add_argument("--refresh-source", action="store_true",
                    help="Fetch tags before checking out source refs.")
    ap.add_argument("--skip-pull", action="store_true",
                    help="Skip docker pull for the Redis module-detection image.")
    ap.add_argument("--progress-every", type=int, default=50,
                    help="Print progress every N command rows. Use 0 for phase-only logs.")
    ap.add_argument("--review", action="store_true",
                    help="After the deterministic pass, have a model independently review every "
                         "row and flag disagreements for a human. Advisory only — it never changes "
                         "a label. Requires OPENAI_API_KEY.")
    ap.add_argument("--review-model", default=os.getenv("OPENAI_MODEL", "gpt-4.1"),
                    help="Model for --review. Defaults to OPENAI_MODEL or gpt-4.1.")
    ap.add_argument("--review-workers", type=int, default=6,
                    help="Parallel workers for the --review pass. Default: 6.")
    ap.add_argument("--add-missing-rows", action="store_true",
                    help="Add rows for Redis/Dragonfly commands absent from the curated table "
                         "(internal/hidden commands are always excluded). Off by default: the "
                         "curated table is authoritative and missing commands are reported as tasks.")
    ap.add_argument("--write-table", dest="write_table", action="store_true", default=False,
                    help="Write the deterministic table to --output. NOT the default: without this "
                         "flag the tool only writes artifacts (draft + change log) for review.")
    ap.add_argument("--no-write-table", dest="write_table", action="store_false",
                    help="Explicitly disable the doc write (default behavior).")
    return ap


def main() -> int:
    args = add_cli_args().parse_args()
    # Writing the public doc is opt-in (--write-table) and only for a complete,
    # unfiltered run: a partial-coverage run must never clobber the full table.
    write_table = bool(args.write_table) and not args.filter and not args.limit
    if args.write_table and not write_table:
        progress("--write-table ignored: --filter / --limit runs never write the public table")

    progress("resolving source checkouts")
    redis_source_root = resolve_redis_source(args)
    dragonfly_source_root = resolve_dragonfly_source(args)
    if not redis_source_root:
        print("ERROR: a Redis source checkout is required for command specs.", file=sys.stderr)
        return 2
    if not dragonfly_source_root:
        print("ERROR: a Dragonfly source checkout is required.", file=sys.stderr)
        return 2

    before, all_rows, after = parse_compat_table(args.input)

    progress(f"loading Redis command specs from {redis_source_root}")
    redis_specs = load_redis_specs_from_checkout(redis_source_root)
    progress(f"Redis core specs: {len(redis_specs)} command(s)")
    # Module command surfaces (options/tokens) are MANDATORY: the exact versions
    # are read from the image's MODULE LIST (drift-proof; falls back to the
    # pinned defaults offline), and specs come from the module repos at that ref.
    try:
        module_dirs = resolve_module_sources(args)
        module_specs = load_module_specs(module_dirs)
    except Exception as e:  # noqa: BLE001
        print(f"ERROR: module command specs are mandatory but could not be loaded: {e}",
              file=sys.stderr)
        return 2
    if not module_specs:
        print("ERROR: module command specs are mandatory but none were loaded.", file=sys.stderr)
        return 2
    redis_specs.update(module_specs)
    module_versions = module_source_versions(module_dirs)
    progress(
        f"module specs merged: {len(module_specs)} command(s) "
        f"({', '.join(f'{k} {v}' for k, v in sorted(module_versions.items()))}); "
        f"total Redis+module specs: {len(redis_specs)}"
    )

    progress("indexing Dragonfly source")
    df = DragonflySource(dragonfly_source_root)
    progress(f"Dragonfly registered commands: {len(df.registered)}")

    # The curated table owns the row SET; the labels are recomputed. By default we
    # do not restructure it — commands missing from it are reported as tasks.
    extra_tasks: list[dict[str, Any]] = []
    if args.add_missing_rows:
        all_rows = add_missing_redis_rows(all_rows, redis_specs)
        all_rows = add_missing_dragonfly_rows(all_rows, df.registered, redis_specs)
    else:
        extra_tasks = missing_command_tasks(all_rows, redis_specs, df.registered)
        if extra_tasks:
            progress(f"commands missing from curated table (reported as tasks): {len(extra_tasks)}")

    rows = filter_rows(all_rows, args.filter)
    if args.limit:
        rows = rows[:args.limit]
    progress(f"compatibility rows selected: {len(rows)} of {len(all_rows)}")

    progress("assessing (deterministic source analysis)")
    assessments = build_assessments(rows, redis_specs, df, args.progress_every)
    progress(f"assessments complete: {len(assessments)} row(s)")

    # Optional independent model review of every row's deterministic verdict.
    # Advisory only: it flags rows for a human, never changes a label.
    review_flags: list[dict[str, Any]] = []
    if args.review:
        review_flags = review_assessments(
            assessments, redis_specs, df, args.review_model,
            args.review_workers, args.progress_every)
        extra_tasks = (extra_tasks or []) + review_flags

    draft_rows, change_log = assessments_to_rows(all_rows, assessments)

    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    out_dir = COMPAT_GENERATED / ts
    progress(f"writing artifacts to {out_dir.relative_to(REPO_ROOT)}")
    write_artifacts(out_dir, before, after, rows, assessments, args,
                    draft_rows=draft_rows, change_log=change_log,
                    extra_tasks=extra_tasks, module_versions=module_versions)

    if write_table:
        applied = [t for t in change_log if t.get("type") == "status-change-applied"]
        args.output.write_text(
            render_compat_table(before, draft_rows, after, verification_note(args)),
            encoding="utf-8",
        )
        print("")
        print(f"Write summary: {len(applied)} label(s) updated from source analysis.")
        print(f"  wrote {display_path(args.output)}")

    return print_summary(assessments, out_dir, write_table, extra_tasks=extra_tasks,
                         review_flags=review_flags)


if __name__ == "__main__":
    sys.exit(main())
