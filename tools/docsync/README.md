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
├── compat_sync.py              # build command compatibility evidence + draft
├── docs_sync.py                # update doc pages from a tag-to-tag source diff
├── openai_llm.py               # shared Responses API + Structured Outputs adapter
├── test_compat_sync.py         # offline source-checkout regression tests
├── test_openai_llm.py          # offline adapter/schema/routing tests
├── dfly_facts.py               # helper — Docker → JSON ground truth
└── requirements.txt
```

Generated artifacts live under `tools/generated/` and are gitignored:

```
tools/generated/
├── facts/<tag>.json            # output of dfly_facts.py
├── compatibility/<ts>/          # compat_sync evidence + draft table
├── source/<tag>.json           # parsed ABSL_FLAG / enum data (flags_sync)
├── update_plans/plan_<ts>.json     # output of docs_sync Phase 1
├── update_plans/results_<ts>.json  # output of docs_sync Phase 2
└── llm_debug/                  # rejected LLM outputs for inspection:
                                #   *_validation_failed_<ts>.md — validation failure
                                #   *_rejected_<file>_<ts>.md   — structural rejection
```

## Setup

```sh
pip install -r tools/docsync/requirements.txt
docker pull docker.dragonflydb.io/dragonflydb/dragonfly:v1.38.0
# compat_sync needs NO API key by default (deterministic source analysis).
export OPENAI_API_KEY=...       # required for every optional LLM step
# Optional global overrides:
export OPENAI_MODEL=gpt-5.6-sol
export OPENAI_REASONING_EFFORT=medium
```

All LLM calls use the OpenAI Responses API with strict Structured Outputs and
`store=False`. Quality-sensitive page/flag updates default to `gpt-5.6-sol`.
Discovery, ACL repair, and the high-volume compatibility review default to
`gpt-5.6-terra`. `OPENAI_MODEL` overrides both defaults (set it to
`gpt-5.6-sol` to run every workflow quality-first).
`OPENAI_REASONING_EFFORT` accepts `none`, `low`, `medium`, `high`, `xhigh`, or
`max`; it defaults to `medium` for GPT-5.6-family models. Set it to `default` to
omit the parameter when overriding to a model with different reasoning support.
Any override must support the Responses API, strict JSON Schema outputs, and
the workflow's configured output cap (up to 64K tokens for `flags_sync.py`).

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

2. **LLM repair pass** (requires `OPENAI_API_KEY`) — for every page
   that the mechanical pass could not handle (no ACL line on a page that
   documents a real server command, multiple ACL lines, etc.) The model is
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

## compat_sync.py

Rebuilds `docs/command-reference/compatibility.md` from **source ground truth —
no LLM, no runtime probing**. Every support label is derived deterministically
from the Redis command specs and the Dragonfly source tree, so the same
checkouts always produce the same table and a new Dragonfly/Redis version is
handled by re-reading the sources. (This replaced an earlier LLM pipeline whose
labels were non-deterministic and often wrong — output differences read as gaps,
hallucinated option lists, run-to-run flips.)

The curated table owns the **row set**; the **labels are recomputed**. The table
is never restructured — commands present in Redis/Dragonfly but missing from it
are reported as `missing-row` tasks, not injected (opt in with
`--add-missing-rows`). Writing the doc is **opt-in** (`--write-table`); by
default the tool only writes review artifacts under
`tools/generated/compatibility/<ts>/`. Docker is used **only** to detect module
versions.

**How each label is decided**, per curated row:

1. **Existence** — is the command registered in the Dragonfly source
   (`CI{"NAME", …}`)? A subcommand (`CONFIG GET`, `SCRIPT LOAD`) exists iff it is
   registered directly, **or** the parent is registered and the parent's
   implementation parses the subcommand token. Not in Dragonfly but in Redis →
   `unsupported`. In Dragonfly with no Redis spec → `dragonfly-specific`.
2. **Options** — for each Redis option token of the command (from the
   version-tracked spec), is it **honored** in the command's Dragonfly
   implementation? A token counts only as a string **literal** (`"DIALECT"`, not
   the bare word — bare `DB` matched `db_index` variables) and **not** when it
   appears only inside an explicit rejection (`"SHUTDOWN ABORT is not supported"`,
   `"COMMAND DOCS Not Implemented"` — recognized but stubbed). Any genuinely
   absent/stubbed → `partial` `Missing: <tokens>.`; none → `supported`.
   Subcommand existence uses only the code reachable from the command's **own**
   public handler, so the internal `DFLYCLUSTER FLUSHSLOTS` dispatch is not
   mistaken for public `CLUSTER FLUSHSLOTS`.

The label is **surface capability**, not behavior: output/value differences,
precision, ordering, a bug, an intentional behavior change, and error-response
differences never reduce support. That is why `FT.INFO` (returns fewer stats
fields but accepts the command) is `Fully supported`, and `SORT` (parses
`BY`/`ASC`/`DESC` in `SortGeneric`) is `Fully supported`. Conversely, an option
the command **silently accepts but does not honor** (a catch-all that ignores it
with no effect, e.g. the `FT.SEARCH` options behind *"unsupported parameters are
ignored for now"*) is a gap, exactly like a rejected one → `partial`. "Honored"
means the option token is genuinely parsed, not merely tolerated.

**The engine — `DragonflySource`.** It indexes every command registration and
function definition once, then per command returns the full implementation text,
**following delegation across files** so options parsed in helpers or sibling
files are visible:

- `SORT` → `SortGeneric`; `ACL SETUSER` → `SetUser` → `ParseAclSetUser`;
- `SCRIPT` → `script_mgr.cc`; `MEMORY USAGE` → `memory_cmd.cc` (cross-file);
- `SCAN` → `ScanOpts::TryFrom` in `common.cc` (a class-qualified call is matched
  on the class, so a generic method name resolves to the right file);
- `FT.*` → the whole `src/server/search/` directory.

An unqualified generic callee (`Parse`, `Run`) is only followed into a file of
the same command family (matching the `family_mgr.cc` / `family_cmd.cc`
convention), so it can't drag in an unrelated family's code. The handler file's
**file-scope string constants** are appended too, because some option tokens are
compared via a `const char* X = "AND"` that never appears in a walked body (e.g.
`BITOP`'s ops). Test files are excluded; the brace matcher skips
comments/strings/char-literals and C++ digit separators (`100'000`) so neither
can truncate a capture. Option presence then greps that text; punctuation-only
tokens (`~`, `=`) are skipped. A corrupted curated row name found in **neither**
source keeps its curated label and is flagged (`unresolved-command`), never
guessed.

**Redis modules are mandatory.** Core Redis has no module command surfaces, so
the tool reads the exact module versions from the Redis image's `MODULE LIST`
(drift-proof; falls back to pinned defaults when Docker is unavailable) and loads
each module's `commands.json` from its repo at that version
(`RediSearch`/`RedisJSON`/`RedisBloom` [BF/CF/CMS/TOPK]/`RedisTimeSeries`). The
resolved `tag@sha` is recorded in `metadata.json`; the run **aborts** if module
specs cannot be loaded. Override with `--module-ref search=v8.6.7`.

```sh
# Recompute labels + write draft/change log; does NOT write the doc:
python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4
# Same, then apply the recomputed labels to compatibility.md after review:
python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4 --write-table
```

Source checkouts are cached under `/tmp`. When a requested ref is missing from a
stale cache, the tool fetches tags and retries automatically. Use
`--refresh-source` to fetch before every checkout.

Artifacts under `tools/generated/compatibility/<ts>/`:

- `assessments.json` — per-row status, `Missing:` details, and source evidence.
- `tasks.json` — `status-change-applied` (every label change vs the curated
  table, with evidence), `missing-row` (commands absent from the table),
  `unresolved-command` (a name in neither source — verify by hand), and
  `placeholder-row`.
- `unsupported_commands.{json,md}` — convenience list of unsupported commands.
- `draft_table.md` — the recomputed table, byte-identical to what
  `--write-table` writes.

**Model review (`--review`, opt-in).** The deterministic core is the authority,
but its source heuristic can still be wrong — a subcommand Dragonfly *recognizes*
but stubs with a "Not Implemented" error (e.g. `COMMAND DOCS`), a fundamental
option mis-listed as missing (e.g. `BITOP AND`), or spec-artifact noise
(`FT.AGGREGATE` function names). So `--review` has a model **independently review
every row** against the Redis spec + Dragonfly source excerpt and flag
disagreements. It is **advisory: it never changes a label** — it produces
`review-flag` tasks with a concrete concern and a suggested status, and the run
summary lists them. The shipped table stays fully deterministic; the model is a
second pair of eyes at scale, not the decider (which is why the LLM-only tool
failed). Needs `OPENAI_API_KEY` (`--review-model`, default `gpt-5.6-terra`); the
default run needs no key.

If one or more model calls fail, the tool records `review-error` tasks and still
writes the deterministic table/artifacts plus all successful reviews. It then
returns exit code 2 so an incomplete review cannot be mistaken for a complete
one.

```sh
# deterministic + model review of every row (flags disagreements, labels unchanged):
python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4 --review
```

**Reviewing a run:** without `--review`, the change log in `tasks.json` is short
and source-grounded — review those changes, not all 400 rows. With `--review`,
also work the `review-flag` list. Version drift (Redis adds an option, Dragonfly
drops one) shows up automatically: the deterministic pass recomputes option
presence each run, so a new/removed option flips the label and appears in the
change log, and the review flags whether it is a real gap.

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

3. **LLM polish** (requires `OPENAI_API_KEY`). The OpenAI model receives the
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
   never the raw diff), walks every `.md` under `docs/`, and asks OpenAI
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
     OpenAI with strict rules:
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

## Typical workflow

```sh
# 1. Targeted, deterministic syncs (cheap, no diff range needed).
python tools/docsync/acl_sync.py    --tag v1.38.0
python tools/docsync/flags_sync.py  --tag v1.38.0

# 2. Recompute the command compatibility table (deterministic; no API key).
#    Review the change log, then re-run with --write-table to apply it.
python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4
python tools/docsync/compat_sync.py --dragonfly-ref v1.39.0 --redis-ref 8.6.4 --write-table

# 3. Cross-page content sync between two releases (LLM-driven, expensive
#    — only run when there is a real release-to-release jump to process).
#    Start with --discover-only to review the plan, then run Phase 2.
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 --discover-only
python tools/docsync/docs_sync.py --update-only-from \
    tools/generated/update_plans/plan_<ts>.json --after v1.38.0

# 4. Read the failure summaries each script printed and fix anything that
#    needs human judgement (FAILED list, llm_debug/ for rejected outputs).

# 5. Verify the build.
yarn build
```

## dfly_facts.py (helper)

Boots `docker.dragonflydb.io/dragonflydb/dragonfly:<tag>`, captures
`COMMAND`, `ACL CAT`, `INFO`, `CONFIG GET *` and parses
`dragonfly --helpfull`, then writes a JSON snapshot under
`tools/generated/facts/<tag>.json`.

Sync scripts call this on demand and reuse the cached file when present.
It can also be run by hand:

```sh
python tools/docsync/dfly_facts.py --tag v1.38.0
python tools/docsync/dfly_facts.py --tag v1.38.0 --skip-pull
```

The `data` portion of the output is bit-stable across runs on the same
tag (`jq -S .data <out>.json | sha256sum` is identical between runs).
The `meta` portion is volatile by design (timestamp, host-dependent
runtime config).
