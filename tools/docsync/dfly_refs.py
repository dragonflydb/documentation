#!/usr/bin/env python3
"""dfly_refs.py — Pin a Dragonfly tag to one commit across source, image and facts.

A release tag is not immutable while its GitHub release is still a draft:
v2.0.0 was force-moved upstream before publication. The docsync scripts read
three things keyed only by the tag name — the source checkout, the Docker
image, and the cached `tools/generated/facts/<tag>.json` — so a moved tag or a
rebuilt image used to go unnoticed. This module resolves the tag to a commit
and lets every script check that all three agree before using them.

The commit of a Docker image comes from `dragonfly --version`, which embeds the
full build SHA (`dragonfly v2.0.0-40553fd8...`).
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import urlparse

DRAGONFLY_REPO = "https://github.com/dragonflydb/dragonfly.git"
DFLY_FACTS = Path(__file__).resolve().parent / "dfly_facts.py"
LS_REMOTE_TIMEOUT_S = 30
FETCH_TIMEOUT_S = 300

# Remotes (by host) that already failed to answer in this process, so a hanging
# network costs one timeout, not one per repository.
_unreachable_hosts: set[str] = set()

ANSI_RE = re.compile(r"\x1b\[[\d;]*m")
VERSION_SHA_RE = re.compile(r"-([0-9a-f]{40})\b")


def run(cmd: list[str], cwd: Path | None = None,
        timeout: float | None = None) -> subprocess.CompletedProcess:
    """subprocess.run that reports a missing binary or a timeout as a failed
    process, so callers only ever check returncode."""
    try:
        return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, check=False,
                              timeout=timeout, env={**os.environ, "GIT_TERMINAL_PROMPT": "0"})
    except OSError as e:
        return subprocess.CompletedProcess(cmd, 127, "", f"cannot run {cmd[0]}: {e}")
    except subprocess.TimeoutExpired:
        return subprocess.CompletedProcess(cmd, 124, "", f"{cmd[0]} timed out after {timeout}s")


def failure_detail(p: subprocess.CompletedProcess) -> str:
    return (p.stderr or p.stdout or "").strip() or f"exit code {p.returncode}"


def short(commit: str | None) -> str:
    return commit[:12] if commit else "?"


# --- Git ----------------------------------------------------------------------

def resolve_commit(checkout: Path, ref: str) -> str | None:
    """Commit SHA that `ref` resolves to in `checkout`, or None."""
    p = run(["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"], cwd=checkout)
    return p.stdout.strip() if p.returncode == 0 and p.stdout.strip() else None


def local_tag_commit(checkout: Path, tag: str) -> str | None:
    """Commit of the tag named exactly `tag` in `checkout`, or None. Unlike
    resolve_commit(f"refs/tags/{tag}"), `v2~1` is not mistaken for a tag."""
    ref = f"refs/tags/{tag}"
    if run(["git", "show-ref", "--verify", "--quiet", ref], cwd=checkout).returncode != 0:
        return None
    return resolve_commit(checkout, ref)


def upstream_tag_lookup(tag: str, repo: str = DRAGONFLY_REPO) -> tuple[bool, str | None]:
    """(remote reachable, commit the tag points to upstream right now or None if
    there is no such tag). Annotated tags are peeled."""
    host = urlparse(repo).netloc or repo
    if host in _unreachable_hosts:
        return False, None
    p = run(["git", "ls-remote", "--tags", repo, f"refs/tags/{tag}", f"refs/tags/{tag}^{{}}"],
            timeout=LS_REMOTE_TIMEOUT_S)
    if p.returncode != 0:
        _unreachable_hosts.add(host)
        print(f"  WARNING: could not query {repo} ({failure_detail(p)}); tags from "
              f"{host} are not checked against upstream in this run", file=sys.stderr)
        return False, None
    refs = dict(
        (name, sha) for sha, name in
        (line.split("\t", 1) for line in p.stdout.splitlines() if "\t" in line)
    )
    return True, refs.get(f"refs/tags/{tag}^{{}}") or refs.get(f"refs/tags/{tag}")


def upstream_tag_commit(tag: str, repo: str = DRAGONFLY_REPO) -> str | None:
    """Commit the tag points to upstream, or None (no such tag, or unreachable)."""
    return upstream_tag_lookup(tag, repo)[1]


def fetch_tags(checkout: Path) -> subprocess.CompletedProcess:
    """Fetch tags, overwriting local tags that moved upstream and dropping tags
    deleted upstream. A plain `git fetch --tags` refuses to update a moved tag
    ("would clobber existing tag") and leaves the stale commit in place."""
    return run(["git", "fetch", "--quiet", "--force", "--prune", "--prune-tags", "--tags",
                "origin"], cwd=checkout, timeout=FETCH_TIMEOUT_S)


def ensure_tag(checkout: Path, tag: str, repo: str = DRAGONFLY_REPO,
               lookup: tuple[bool, str | None] | None = None) -> str:
    """Commit of `tag` in `checkout`, made to match upstream first.

    Tags are fetched (with --force/--prune-tags) only when the tag is new or moved
    upstream; a tag that no longer exists upstream is an error. If upstream cannot
    be reached, the local tag is used with a warning. Branch names are not
    accepted: they would silently resolve to a stale local ref. `lookup` is an
    already made upstream_tag_lookup(tag, repo) result.
    """
    if not (checkout / ".git").exists():
        checkout.parent.mkdir(parents=True, exist_ok=True)
        print(f"  cloning Dragonfly source to {checkout}...", flush=True)
        p = run(["git", "clone", "--quiet", repo, str(checkout)])
        if p.returncode != 0:
            raise RuntimeError(f"could not clone {repo} to {checkout}: {failure_detail(p)}")
    reachable, upstream = lookup if lookup is not None else upstream_tag_lookup(tag, repo)
    if reachable and not upstream:
        raise RuntimeError(f"Dragonfly tag {tag!r} does not exist upstream in {repo}")
    local = local_tag_commit(checkout, tag)
    fetch = None
    if reachable and local != upstream:
        print(f"  fetching tags into {checkout} ({tag}: local {short(local)}, "
              f"upstream {short(upstream)})...", flush=True)
        fetch = fetch_tags(checkout)
        if fetch.returncode != 0:
            print(f"  WARNING: git fetch in {checkout} failed: {failure_detail(fetch)}",
                  file=sys.stderr)
        local = local_tag_commit(checkout, tag)
    detail = f"; git fetch failed: {failure_detail(fetch)}" if fetch and fetch.returncode else ""
    if not local:
        raise RuntimeError(f"Dragonfly tag {tag!r} does not exist in {checkout}{detail}")
    if upstream and local != upstream:
        raise RuntimeError(f"Dragonfly tag {tag!r} is {short(upstream)} upstream but "
                           f"{short(local)} in {checkout}{detail}")
    return local


def ensure_checkout(checkout: Path, tag: str, repo: str = DRAGONFLY_REPO) -> str:
    """Check out `tag` (see ensure_tag) and verify HEAD. Returns HEAD's SHA."""
    commit = ensure_tag(checkout, tag, repo)
    p = run(["git", "checkout", "--quiet", commit], cwd=checkout)
    if p.returncode != 0:
        raise RuntimeError(f"could not check out Dragonfly {tag} ({short(commit)}) "
                           f"in {checkout}: {failure_detail(p)}")
    head = resolve_commit(checkout, "HEAD")
    if head != commit:
        raise RuntimeError(f"{checkout} is at {short(head)} after checking out "
                           f"{tag} ({short(commit)})")
    # Submodules someone initialized (helio) must follow the tag too; others stay
    # uninitialized.
    run(["git", "submodule", "update", "--recursive"], cwd=checkout)
    # Local edits or untracked files survive a checkout and would be parsed as
    # if they were part of the tag.
    status = run(["git", "status", "--porcelain", "--untracked-files=normal"], cwd=checkout)
    if status.returncode != 0 or status.stdout.strip():
        raise RuntimeError(
            f"{checkout} has local changes, so it does not match {tag} ({short(commit)}): "
            f"{failure_detail(status) if status.returncode else status.stdout.strip()[:200]}. "
            f"Clean it with `git -C {checkout} reset --hard && git -C {checkout} clean -fd "
            f"&& git -C {checkout} submodule update --recursive`."
        )
    print(f"  Dragonfly source: {tag} @ {short(commit)} ({checkout})")
    return commit


# --- Docker -------------------------------------------------------------------

def docker_pull(image_ref: str) -> None:
    print(f"  Pulling {image_ref}...")
    p = run(["docker", "pull", image_ref])
    if p.returncode != 0:
        detail = failure_detail(p)
        hint = ""
        if "not found" in detail or "manifest unknown" in detail:
            tag = image_ref.rsplit(":", 1)[-1]
            hint = (f" (no image is published for {tag}; if its GitHub release is still "
                    f"a draft, build it with tools/docsync/build_prerelease_image.sh {tag} "
                    f"and re-run with --skip-pull)")
        raise RuntimeError(f"docker pull {image_ref} failed: {detail}{hint}")


def image_version(image_ref: str) -> tuple[str, str | None]:
    """(`dragonfly --version` first line, build commit SHA or None) of a local
    image. Never pulls: raises if the image is not present locally."""
    p = run(["docker", "run", "--rm", "--pull=never", "--entrypoint", "dragonfly",
             image_ref, "--version"])
    lines = ANSI_RE.sub("", p.stdout).strip().splitlines()
    if not lines or not lines[0].startswith("dragonfly"):
        tag = image_ref.rsplit(":", 1)[-1]
        raise RuntimeError(
            f"image {image_ref} is not available locally: {failure_detail(p)} "
            f"(run without --skip-pull to pull it, or for a draft release build it with "
            f"tools/docsync/build_prerelease_image.sh {tag})"
        )
    m = VERSION_SHA_RE.search(lines[0])
    return lines[0], (m.group(1) if m else None)


# --- Facts --------------------------------------------------------------------

def facts_commit(facts: dict) -> str | None:
    return (facts.get("meta") or {}).get("dragonfly_commit")


def facts_staleness(facts: dict, tag: str, image_ref: str | None) -> str | None:
    """Why cached facts no longer describe `tag`, or None if they still do.

    Compared against the tag's current upstream commit and, when `image_ref` is
    present locally, the commit of that image.
    """
    cached = facts_commit(facts)
    if not cached:
        return "facts file has no meta.dragonfly_commit (captured before commit tracking)"
    reachable, upstream = upstream_tag_lookup(tag)
    if reachable and not upstream:
        return f"tag {tag} does not exist upstream"
    if upstream and upstream != cached:
        return f"tag {tag} moved upstream to {short(upstream)}, facts are from {short(cached)}"
    if image_ref:
        try:
            _, local = image_version(image_ref)
        except RuntimeError:
            local = None  # not pulled/built yet; the upstream check above still applies
        if local and local != cached:
            return f"local image {image_ref} is at {short(local)}, facts are from {short(cached)}"
    return None


def load_facts(tag: str, facts_dir: Path, image_ref: str, *,
               skip_pull: bool, refresh: bool) -> dict:
    """Load facts_dir/<tag>.json if it still matches the tag's commit; otherwise
    (or with refresh) capture it again via dfly_facts.py."""
    facts_path = facts_dir / f"{tag}.json"
    if facts_path.exists() and not refresh:
        facts = json.loads(facts_path.read_text(encoding="utf-8"))
        stale = facts_staleness(facts, tag, image_ref)
        if stale is None:
            print(f"  using cached facts: {facts_path} "
                  f"(Dragonfly {short(facts_commit(facts))})")
            return facts
        print(f"  cached facts are stale: {stale}; re-capturing", flush=True)
    cmd = [sys.executable, str(DFLY_FACTS), "--tag", tag, "--output", str(facts_path)]
    if skip_pull:
        cmd.append("--skip-pull")
    print("  capturing facts via dfly_facts.py...", flush=True)
    if subprocess.run(cmd).returncode != 0:
        raise RuntimeError("dfly_facts capture failed (see its output above)")
    return json.loads(facts_path.read_text(encoding="utf-8"))


def check_same_commit(tag: str, **commits: str | None) -> None:
    """Raise if the known commits (source, image, facts, ...) disagree."""
    known = {name: c for name, c in commits.items() if c}
    if len(set(known.values())) > 1:
        listing = ", ".join(f"{name}={short(c)}" for name, c in known.items())
        raise RuntimeError(
            f"Dragonfly {tag} inputs are from different commits: {listing}. "
            f"The tag probably moved: rebuild or re-pull the image, then re-run."
        )
