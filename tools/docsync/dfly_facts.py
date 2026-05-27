#!/usr/bin/env python3
"""dfly_facts.py — Capture runtime facts from a Dragonfly Docker image.

Boots the official Dragonfly Docker image at the given tag, queries the live
server for its registered commands, ACL categories, INFO sections and config,
runs `dragonfly --helpfull` in a separate ephemeral container to capture flag
defaults, then tears everything down and writes a JSON snapshot.

This is the runtime oracle for DocSync v2 drift detection. Paired with
source_index.py (static) it provides ground truth for every fact a doc page
might claim.

Usage:
    python tools/docsync/dfly_facts.py --tag v1.38.0
    python tools/docsync/dfly_facts.py --tag v1.38.0 \\
        --output tools/generated/facts/v1.38.0.json
    python tools/docsync/dfly_facts.py --tag v1.38.0 --skip-pull

Output JSON shape (top level):
    {
      "schema_version": 1,
      "tag": "v1.38.0",
      "meta": {
        "captured_at": "2026-...Z",
        "image_digest": "sha256:...",
        "runtime_config": { "maxmemory": "...", ... }   # volatile, host-dependent
      },
      "data": {
        "commands":        { "BITCOUNT": {arity, flags, ...}, ... },
        "acl_categories":  { "@read": ["GET","MGET",...], ... },
        "command_acl":     { "GET": ["@read","@string","@fast"], ... },
        "flags":           { "tiered_storage_write_depth": {default,desc,group}, ... },
        "info_sections":   ["Server","Clients",...]
      }
    }

`data` is bit-stable across runs on the same tag. `meta` is volatile by design
(captured_at varies; runtime_config holds CONFIG GET output where some values
like maxmemory are auto-detected from host memory).
For reproducibility tests: `jq -S .data <out>.json | sha256sum` should be
identical between two runs on the same tag.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import redis

DRAGONFLY_IMAGE = "docker.dragonflydb.io/dragonflydb/dragonfly"
SCHEMA_VERSION = 1
PING_TIMEOUT_S = 30
ANSI_RE = re.compile(r"\x1b\[[\d;]*m")


def run(cmd: list[str], check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, capture_output=True, text=True, check=check)


# --- Docker -------------------------------------------------------------------

def docker_pull(image_ref: str) -> None:
    print(f"  Pulling {image_ref}...")
    run(["docker", "pull", image_ref])


def docker_image_digest(image_ref: str) -> str:
    p = run(["docker", "inspect", "--format", "{{index .RepoDigests 0}}", image_ref], check=False)
    out = p.stdout.strip()
    if "@" in out:
        return out.split("@", 1)[1]
    return ""


def docker_run_dragonfly(image_ref: str, name: str) -> str:
    """Boot Dragonfly detached. Return container IP on bridge network."""
    run(["docker", "run", "-d", "--name", name, image_ref])
    p = run([
        "docker", "inspect", name,
        "--format", "{{.NetworkSettings.Networks.bridge.IPAddress}}",
    ])
    ip = p.stdout.strip()
    if not ip:
        raise RuntimeError(f"could not determine bridge IP for container {name}")
    return ip


def docker_rm(name: str) -> None:
    subprocess.run(["docker", "rm", "-f", name], capture_output=True)


def docker_helpfull(image_ref: str) -> str:
    """Run `dragonfly --helpfull` in an ephemeral container and return raw stdout."""
    p = subprocess.run(
        ["docker", "run", "--rm", "--entrypoint", "dragonfly", image_ref, "--helpfull"],
        capture_output=True, text=True,
    )
    return p.stdout


# --- Connection ---------------------------------------------------------------

def wait_for_ping(ip: str, port: int = 6379, timeout: float = PING_TIMEOUT_S) -> redis.Redis:
    deadline = time.time() + timeout
    last_err: Exception | None = None
    while time.time() < deadline:
        try:
            r = redis.Redis(host=ip, port=port, socket_timeout=2, decode_responses=True)
            if r.ping():
                return r
        except (redis.RedisError, OSError) as e:
            last_err = e
        time.sleep(0.3)
    raise RuntimeError(f"Dragonfly never responded to PING within {timeout}s ({last_err})")


# --- Fact capture -------------------------------------------------------------

def capture_commands(r: redis.Redis) -> dict:
    """COMMAND → {NAME: {arity, flags, first_key_pos, last_key_pos, step_count}}.

    redis-py 7.x returns this already parsed as a dict.
    Sub-commands (e.g. ACL DELUSER) are top-level keys.
    """
    raw = r.execute_command("COMMAND")
    out: dict[str, dict] = {}
    if isinstance(raw, dict):
        for name, entry in raw.items():
            if isinstance(entry, dict):
                out[name.upper()] = {
                    "arity": entry.get("arity"),
                    "flags": sorted(entry.get("flags", []) or []),
                    "first_key_pos": entry.get("first_key_pos"),
                    "last_key_pos": entry.get("last_key_pos"),
                    "step_count": entry.get("step_count"),
                }
    elif isinstance(raw, list):
        # Older redis-py: list-of-lists fallback
        for entry in raw:
            if isinstance(entry, list) and len(entry) >= 6:
                name = (entry[0] or "").upper()
                out[name] = {
                    "arity": entry[1],
                    "flags": sorted(entry[2] or []),
                    "first_key_pos": entry[3],
                    "last_key_pos": entry[4],
                    "step_count": entry[5],
                }
    return dict(sorted(out.items()))


def capture_acl(r: redis.Redis) -> tuple[dict, dict]:
    """Return (acl_categories, command_acl).

    acl_categories: {"@read": ["GET","MGET",...], ...}
    command_acl:    {"GET": ["@read","@fast","@string"], ...}  (inverted, per-command)
    """
    cats_raw = r.execute_command("ACL", "CAT") or []
    cats = sorted(c.lower() for c in cats_raw if isinstance(c, str))
    acl_categories: dict[str, list[str]] = {}
    command_acl: dict[str, list[str]] = {}
    for cat in cats:
        # ACL CAT accepts the lowercase form too
        members = r.execute_command("ACL", "CAT", cat) or []
        members_clean = sorted(m.upper() for m in members if isinstance(m, str))
        acl_categories[f"@{cat}"] = members_clean
        for m in members_clean:
            command_acl.setdefault(m, []).append(f"@{cat}")
    for m in command_acl:
        command_acl[m] = sorted(set(command_acl[m]))
    return dict(sorted(acl_categories.items())), dict(sorted(command_acl.items()))


def capture_info_sections(container_name: str) -> list[str]:
    """Return INFO section names by shelling out to redis-cli inside the container.

    redis-py 7.x auto-parses INFO into a flat dict and drops `# Section` markers,
    so we get raw text via the bundled redis-cli instead.
    """
    p = run(["docker", "exec", container_name, "redis-cli", "INFO"])
    sections = []
    for line in p.stdout.split("\n"):
        line = line.strip()
        if line.startswith("# "):
            sections.append(line[2:].strip())
    return sorted(set(sections))


def capture_config(r: redis.Redis) -> dict:
    """CONFIG GET * → dict (sorted)."""
    raw = r.execute_command("CONFIG", "GET", "*")
    out: dict[str, str] = {}
    if isinstance(raw, dict):
        out = {str(k): str(v) for k, v in raw.items()}
    elif isinstance(raw, list):
        # Even-indexed = keys, odd = values
        for k, v in zip(raw[0::2], raw[1::2]):
            out[str(k)] = str(v)
    return dict(sorted(out.items()))


# --- --helpfull parser --------------------------------------------------------

_FLAG_START_RE = re.compile(r"^\s+--([a-z][a-z0-9_]*)\s+\(")
_FLAGS_FROM_RE = re.compile(r"^\s*Flags from\s+(.+?):\s*$")
_FLAG_BODY_RE = re.compile(
    r"^--(?P<name>[a-z][a-z0-9_]*)\s*"
    r"\((?P<desc>.*?)\)\s*;?\s*"
    r"(?:type:\s*(?P<type>\S+);?\s*)?"
    r"default:\s*(?P<default>.*?);?\s*$",
    re.DOTALL,
)


def parse_helpfull(text: str) -> dict:
    """Parse `dragonfly --helpfull` output into {flag: {default, description, type, group}}.

    Handles multi-line description blocks and ANSI color codes around filenames.
    """
    text = ANSI_RE.sub("", text)
    lines = text.split("\n")
    flags: dict[str, dict] = {}
    current_group: str | None = None
    i = 0
    while i < len(lines):
        line = lines[i]
        m = _FLAGS_FROM_RE.match(line)
        if m:
            current_group = m.group(1).strip()
            i += 1
            continue
        if _FLAG_START_RE.match(line):
            block = [line.strip()]
            i += 1
            while i < len(lines):
                nxt = lines[i]
                if _FLAG_START_RE.match(nxt) or _FLAGS_FROM_RE.match(nxt):
                    break
                if nxt.strip() == "":
                    # Two empty lines in a row = end of block
                    if i + 1 < len(lines) and lines[i + 1].strip() == "":
                        break
                    i += 1
                    continue
                block.append(nxt.strip())
                # Block typically ends on a line containing "default: ...;"
                if re.search(r"\bdefault:\s*[^;]*;\s*$", nxt):
                    i += 1
                    break
                i += 1
            joined = " ".join(block)
            mb = _FLAG_BODY_RE.match(joined)
            if mb:
                desc = re.sub(r"\s+", " ", mb.group("desc")).strip()
                default = mb.group("default").rstrip(";").strip()
                ftype = (mb.group("type") or "").strip().rstrip(";") or None
                flags[mb.group("name")] = {
                    "default": default,
                    "description": desc,
                    "type": ftype,
                    "group": current_group,
                }
            continue
        i += 1
    return dict(sorted(flags.items()))


# --- Atomic write -------------------------------------------------------------

def write_atomic_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    os.replace(tmp, path)


# --- Main ---------------------------------------------------------------------

def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    p.add_argument("--tag", required=True, help="Dragonfly tag (e.g. v1.38.0)")
    p.add_argument("--output", type=Path, default=None,
                   help="Output JSON path. Default: tools/generated/facts/<tag>.json relative to repo root.")
    p.add_argument("--skip-pull", action="store_true",
                   help="Skip docker pull (use already-cached image).")
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parents[2]
    output = args.output or repo_root / "tools" / "generated" / "facts" / f"{args.tag}.json"
    image_ref = f"{DRAGONFLY_IMAGE}:{args.tag}"
    container_name = f"dfly-facts-{args.tag.replace('.', '-')}-{os.getpid()}"

    print(f"[1/5] Image {image_ref}")
    if not args.skip_pull:
        docker_pull(image_ref)
    image_digest = docker_image_digest(image_ref)

    print(f"[2/5] Capture --helpfull (ephemeral container)...")
    helpfull_raw = docker_helpfull(image_ref)
    flags = parse_helpfull(helpfull_raw)
    print(f"  parsed {len(flags)} flags")

    print(f"[3/5] Boot {container_name}...")
    try:
        ip = docker_run_dragonfly(image_ref, container_name)
        print(f"  IP: {ip}")
        r = wait_for_ping(ip)

        print("[4/5] Capture runtime facts...")
        commands = capture_commands(r)
        print(f"  COMMAND: {len(commands)} entries")
        acl_categories, command_acl = capture_acl(r)
        print(f"  ACL CAT: {len(acl_categories)} categories, {len(command_acl)} command mappings")
        info_sections = capture_info_sections(container_name)
        print(f"  INFO sections: {info_sections}")
        config = capture_config(r)
        print(f"  CONFIG: {len(config)} entries")
    finally:
        docker_rm(container_name)

    payload = {
        "schema_version": SCHEMA_VERSION,
        "tag": args.tag,
        "meta": {
            "captured_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "image_digest": image_digest,
            "runtime_config": config,
        },
        "data": {
            "commands": commands,
            "acl_categories": acl_categories,
            "command_acl": command_acl,
            "info_sections": info_sections,
            "flags": flags,
        },
    }

    print(f"[5/5] Write {output}")
    write_atomic_json(output, payload)
    print(f"  wrote {output} ({output.stat().st_size:,} bytes)")
    print(f"\nReproducibility check:")
    print(f"  jq -S .data {output} | sha256sum")
    return 0


if __name__ == "__main__":
    sys.exit(main())
