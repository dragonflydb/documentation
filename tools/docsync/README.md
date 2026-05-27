# docsync

Production scripts that keep `docs/` in sync with the running Dragonfly
server. Each script is end-to-end: it captures ground truth from a
Dragonfly Docker image (and, where useful, the C++ source), applies the
smallest possible change to the docs, and reports anything it could not
fix.

## Layout

```
tools/docsync/
├── acl_sync.py                 # update **ACL categor(y|ies):** lines
├── flags_sync.py               # update flag defaults + add new flags
├── docs_sync.py                # update doc pages from a tag-to-tag source diff
├── propose_change_message.py   # write a commit/PR title+body for the diff
├── dfly_facts.py               # helper — Docker → JSON ground truth
└── requirements.txt
```

Generated artifacts live under `tools/generated/` and are gitignored:

```
tools/generated/
├── facts/<tag>.json            # output of dfly_facts.py
├── source/<tag>.json           # parsed ABSL_FLAG / enum data (flags_sync)
├── update_plans/plan_<ts>.json     # output of docs_sync Phase 1
├── update_plans/results_<ts>.json  # output of docs_sync Phase 2
├── change_messages/*.md        # output of propose_change_message.py
└── llm_debug/                  # raw LLM responses for inspection:
                                #   *_<ts>.txt      — JSON-parse failure
                                #   *_validation_failed_<ts>.md — validation failure
                                #   *_rejected_<file>_<ts>.md   — structural rejection
```

## Setup

```sh
pip install -r tools/docsync/requirements.txt
docker pull docker.dragonflydb.io/dragonflydb/dragonfly:v1.38.0
export ANTHROPIC_API_KEY=...    # required for: flags_sync LLM polish,
                                # docs_sync (both phases), acl_sync repair pass,
                                # propose_change_message
```

## acl_sync.py

Captures `ACL CAT` from the live server and updates the `**ACL
categor(y|ies):**` line on every command-reference page whose H1 matches
a server command. Two stages:

1. **Mechanical pass** — minimal-diff edits:
   - if the *set* of categories on a page already equals the server set,
     the file is **not touched at all**;
   - when the set differs, categories that stay keep their original
     order, new ones are appended (alphabetically), removed ones are
     dropped.

2. **LLM repair pass** (requires `ANTHROPIC_API_KEY`) — for every page
   that the mechanical pass could not handle (no ACL line on a page that
   documents a real server command, multiple ACL lines, etc.) Claude is
   given the page text, the command name, the expected categories from
   the server, and detailed instructions:
   - if the page is a container / navigation page (body is mostly a list
     of subcommand pages, language like "This is a container command for
     ..."), classify it as overview and skip — no edit;
   - otherwise insert exactly one new line of the form `**ACL
     categories:** @cat1, @cat2, ...` directly after `**Time
     complexity:**` (or after the H1 + Syntax block if there is no Time
     complexity line), mirroring the surrounding bullet/plain style.
   The LLM output is *validated*: the patched page must contain exactly
   one ACL line whose category set matches the server. If validation
   fails the patch is rejected and the page stays in the FAILED list.

Pages that remain in FAILED after both stages are listed at the end of
the run with the LLM's complaint appended — they need a human to look.

```sh
python tools/docsync/acl_sync.py --tag v1.38.0
python tools/docsync/acl_sync.py --tag v1.38.0 --dry-run
python tools/docsync/acl_sync.py --tag v1.38.0 --no-llm        # mechanical-only
python tools/docsync/acl_sync.py --tag v1.38.0 --filter "search/*"
python tools/docsync/acl_sync.py --facts tools/generated/facts/v1.38.0.json
```

Exit code is non-zero if any page is reported as FAILED after both
passes.

## flags_sync.py

Synchronizes `docs/managing-dragonfly/flags.md` with the server.
Three-stage pipeline:

1. **Capture facts** from two sources:
   - Docker (`dfly_facts.py`) — authoritative defaults, types, groups, and
     the short `--helpfull` description.
   - C++ source (parsed inline; the script clones the Dragonfly repo to
     `/tmp/dragonfly-docsync` and checks out the requested tag) — gives
     the ABSL_FLAG declaration's file/line, surrounding C++ comments, and
     for enum-typed flags the enum's value list with positional indices.
     Cached in `tools/generated/source/<tag>.json`.

2. **Mechanical pass.**
   - **Delete** sections for flags the server no longer reports. The
     binary is the authoritative source: if a flag isn't there the doc
     was wrong and the section is dropped.
   - For each remaining flag, replace the single `default: ...` line if
     the value differs. A byte-equivalence check skips cosmetic
     reformatting (`0` vs `0B`, `128MiB` vs `128.00MiB`, `65536` vs
     `64.0KiB`). **Enum-typed defaults** (doc has a number, server reports
     an uppercase enum constant, e.g. `compression_mode: 3 →
     MULTI_ENTRY_LZ4`) are NOT mechanically rewritten: keeping the
     integer is what the CLI accepts, and the LLM polish is responsible
     for adding the enum-value table to the description.

3. **LLM polish** (requires `ANTHROPIC_API_KEY`). Claude receives the
   mechanically-fixed page, the full ground-truth dict, the source-facts
   dict (with C++ comments and enum tables), the list of flags to add,
   the list to keep-even-though-removed, and the list of enum defaults to
   expand. It produces a polished page that:
   - keeps existing flag descriptions verbatim where facts already match;
   - integrates new C++ comment context only when it adds real value;
   - writes descriptions for flags missing from the doc using the help
     text + source comments;
   - for enum-typed defaults, keeps the integer in `default:` and adds a
     value table to the description body.
   The LLM output is validated (every server flag present, defaults match
   modulo byte equivalence, enum defaults still integers). If validation
   fails the LLM output is discarded and the mechanical-only result stays
   on disk. The raw response is saved under `tools/generated/llm_debug/`
   for inspection.

Upstream `glog-src/` and `abseil_cpp-src/` flags are filtered out of
auto-add (but their defaults are still corrected if a human chose to
document them).

```sh
python tools/docsync/flags_sync.py --tag v1.38.0
python tools/docsync/flags_sync.py --tag v1.38.0 --dry-run
python tools/docsync/flags_sync.py --tag v1.38.0 --no-llm        # mechanical only
python tools/docsync/flags_sync.py --tag v1.38.0 --skip-source   # no C++ context
python tools/docsync/flags_sync.py --tag v1.38.0 --refresh-source
python tools/docsync/flags_sync.py --facts tools/generated/facts/v1.38.0.json
```

Flags that the doc still lists but the server no longer reports are
**deleted** during the mechanical pass and listed in the run summary so
the change is visible. The server is the authoritative source — if a
flag isn't reported, documenting it would mislead users.

## docs_sync.py

Updates documentation pages whose content drifted between two Dragonfly
releases. Two phases driven by one command:

1. **Discover** (single LLM call). Computes the Dragonfly source diff
   between `--before` and `--after` (commit subjects + per-file stat,
   never the raw diff), walks every `.md` under `docs/`, and asks Claude
   which pages plausibly need updating and why. The plan is saved to
   `tools/generated/update_plans/plan_<ts>.json`.

   An optional `--also-update FILE` adds explicit paths to the plan
   regardless of LLM judgement (one path per line, comments with `#`
   ignored). These are **forced overrides** — they are always processed
   even if the LLM decided no change is needed.

2. **Update** (one LLM session per file). For each file in the plan:
   - Read the current page.
   - Identify the topic from the H1; if it matches a real server command,
     pull the C++ handler body from the Dragonfly checkout at `--after`
     and the `COMMAND` / `ACL CAT` data captured by `dfly_facts.py`.
   - Boot a Dragonfly container at `--after` (with `--cluster_mode=emulated`
     for cluster-family commands).
   - Pick a **sibling page** in the same directory as a *style template*
     (the shortest sibling that has H2 sections). The LLM is told to
     mirror the sibling's structural / formatting conventions and never
     introduce a style that would make the page look different from its
     siblings.
   - Build a `diff_context` payload only for files that came from the
     Phase-1 LLM discovery: the discovery `reason` plus the list of
     commits between `--before` and `--after` that touched each related
     source file. This focuses the update session on what actually
     changed. Files added via `--also-update` get `diff_context: null` —
     they are reviewed against the **whole** current source state, with
     no implicit assumption about which area needs attention.
   - Send the page + source + sibling style + `diff_context` (or null) to
     Claude with strict rules:
       * only assert facts the inputs support;
       * **general-case complexity only**, no edge cases;
       * never invent options or behaviors;
       * preserve frontmatter / `<PageTitle>`;
       * preserve any human-written content the source/Docker cannot
         refute;
       * **match the existing visual style exactly** (heading levels,
         metadata block style, parameter / example framing, link
         convention) — change CONTENT not FORM;
       * **do NOT modify the `**ACL categor(y|ies):**` line** — that
         metadata is owned by `acl_sync.py` and must stay byte-identical;
       * **do NOT change page structure** — keep every existing section
         in place, do not add new top-level sections, do not move or
         append example blocks. New examples must be placed inside the
         page's existing `## Examples` section, beside related ones;
       * never write a bare `<placeholder>` outside a fenced code block.
   - **Structural validation** runs first. Catches catastrophic LLM
     failures: output shorter than 80 non-whitespace chars, output
     shrunk to less than half of input, output that's just `...`,
     missing frontmatter / H1 / `<PageTitle>` / `import PageTitle`,
     dropped H2 sections, modified ACL line. On any failure the run is
     marked `failed`, the raw LLM markdown is saved to
     `tools/generated/llm_debug/docs_sync_rejected_<file>_<ts>.md`, and
     the file on disk is **not touched**.
   - **Docker verification**: the caller walks every `dragonfly>`
     invocation in the LLM's markdown and runs it in Docker, substituting
     whatever output the LLM wrote with the actual server output.
     **`FLUSHALL` is issued before every ```shell``` block** so prior
     examples never leak into the next — each block starts from a clean
     keyspace. Within a block state persists, so a chain like `SET k 1`
     → `GET k` works. Non-zero exits are noted but the captured stderr
     replaces the LLM's predicted output (so a documented error case
     shows the real error). The LLM is encouraged to extend examples
     with setup commands at the top of a block (e.g. `RPUSH mylist a b c`
     before `LRANGE mylist 0 -1`) when this makes the example clearer.
   - Post-processing safety nets:
       * MDX placeholder wrap — anything the LLM left bare in prose
         (`<key>` → `` `<key>` ``) is escaped, while real HTML elements
         like `<details>` / `<summary>` are recognized and left alone;
       * **byte-identical skip** — if final markdown == input, no write;
       * **cosmetic-only skip** — if the only diff is blank-line counts
         or trailing whitespace, no write. Both prevent noise edits in
         git diff.

```sh
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 \
    --also-update extra_pages.txt
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 \
    --discover-only        # write the plan and stop
python tools/docsync/docs_sync.py \
    --update-only-from tools/generated/update_plans/plan_<ts>.json \
    --after v1.38.0        # skip discovery, run Phase 2 against a saved plan
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 \
    --filter "command-reference/strings/*"
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 --dry-run
```

Per-file results are written to
`tools/generated/update_plans/results_<ts>.json`. Each entry has a
status (`updated`, `unchanged`, `failed`, `skipped`, `missing`, `error`)
and a `notes` list with everything the run noticed: which sibling style
was used, whether `diff_context` was present, how many invocations were
verified in Docker, any non-zero exits, whether MDX safety wrapped
anything, why a write was skipped. Failed entries also point at the
saved raw LLM output under `tools/generated/llm_debug/` so the failure
mode can be inspected without re-running the LLM.

## propose_change_message.py

Reads the working-tree diff (including untracked files via
`git ls-files --others`) and asks Claude for a conventional-commit title
and a Markdown PR body. Writes the result to
`tools/generated/change_messages/<timestamp>.md` and prints it.

The script never runs `git commit` or `gh pr create`. It only proposes
text — you copy it into your own commit / PR.

```sh
python tools/docsync/propose_change_message.py
python tools/docsync/propose_change_message.py --staged
python tools/docsync/propose_change_message.py --base origin/main
python tools/docsync/propose_change_message.py --dump-prompt
```

## Typical workflow

```sh
# 1. Targeted, deterministic syncs (cheap, no diff range needed).
python tools/docsync/acl_sync.py    --tag v1.38.0
python tools/docsync/flags_sync.py  --tag v1.38.0

# 2. Cross-page content sync between two releases (LLM-driven, expensive
#    — only run when there is a real release-to-release jump to process).
#    Start with --discover-only to review the plan, then run Phase 2.
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 --discover-only
python tools/docsync/docs_sync.py --update-only-from \
    tools/generated/update_plans/plan_<ts>.json --after v1.38.0

# 3. Read the failure summaries each script printed and fix anything that
#    needs human judgement (FAILED list, llm_debug/ for rejected outputs).

# 4. Verify the build.
yarn build

# 5. Get a commit/PR message proposal.
python tools/docsync/propose_change_message.py
```

## dfly_facts.py (helper)

Boots `docker.dragonflydb.io/dragonflydb/dragonfly:<tag>`, captures
`COMMAND`, `ACL CAT`, `INFO`, `CONFIG GET *` and parses
`dragonfly --helpfull`, then writes a JSON snapshot under
`tools/generated/facts/<tag>.json`.

Both sync scripts call this on demand and reuse the cached file when
present. It can also be run by hand:

```sh
python tools/docsync/dfly_facts.py --tag v1.38.0
python tools/docsync/dfly_facts.py --tag v1.38.0 --skip-pull
```

The `data` portion of the output is bit-stable across runs on the same
tag (`jq -S .data <out>.json | sha256sum` is identical between runs).
The `meta` portion is volatile by design (timestamp, host-dependent
runtime config).
