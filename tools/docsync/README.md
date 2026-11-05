# docsync

Production scripts that keep `docs/` in sync with the running Dragonfly
server. Each script is end-to-end: it captures ground truth from a
Dragonfly Docker image (and, where useful, the C++ source), applies the
smallest possible change to the docs, and reports anything it could not
fix.

## Layout

```
tools/docsync/
├── acl_sync.py                 # update **ACL categor(y|ies):** lines + the ACL categories page
├── flags_sync.py               # update flag defaults + add new flags
├── compat_sync.py              # build command compatibility evidence + draft
├── docs_sync.py                # update doc pages from a tag-to-tag source diff
├── openai_llm.py               # shared Responses API + Structured Outputs adapter
├── test_compat_sync.py         # offline source-checkout regression tests
├── test_dfly_refs.py           # offline tag/commit consistency tests
├── test_acl_sync.py            # offline subcommand/container/dry-run tests
├── test_flags_sync.py          # offline C++ flag parser / dry-run tests
├── test_openai_llm.py          # offline adapter/schema/routing tests
├── acl_model.py                # helper — which ACL entry the server checks for a command
├── dfly_facts.py               # helper — Docker → JSON ground truth
├── dfly_refs.py                # helper — pins a tag to one commit (source/image/facts)
├── build_prerelease_image.sh   # builds the image for a draft (unpublished) release
└── requirements.txt
```

Generated artifacts live under `tools/generated/` and are gitignored:

```
tools/generated/
├── facts/<tag>.json            # output of dfly_facts.py
├── compatibility/<ts>/          # compat_sync evidence + draft table
├── source/<tag>.json           # parsed ABSL_FLAG / enum data + commit (flags_sync)
├── update_plans/plan_<ts>.json     # output of docs_sync Phase 1
├── update_plans/results_<ts>.json  # output of docs_sync Phase 2
└── llm_debug/                  # rejected LLM outputs for inspection:
                                #   *_validation_failed_<ts>.md — validation failure
                                #   *_rejected_<file>_<ts>.md   — structural rejection
```

## Setup

```sh
pip install -r tools/docsync/requirements.txt
docker pull docker.dragonflydb.io/dragonflydb/dragonfly:v2.1.0
#   (not published yet for a draft release — see "Unreleased tags" below)
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

## Release runbook (run in this order)

One pass per Dragonfly release. Run the scripts **one at a time**:
`docs_sync.py`, `flags_sync.py` and `compat_sync.py` share the source checkout
in `/tmp/dragonfly-docsync`. Review and commit after each step, so every change
can be checked (and reverted) on its own. The code blocks contain no `#`
comments, so they can be pasted into bash or zsh as they are.

**Nothing in this runbook pushes anything, and nothing may be pushed.** The
scripts only read from GitHub and Docker registries, and all their writes are
local. Never `git push` to `dragonflydb/dragonfly`, never `docker push` the
locally built image (it carries the official image name), and never modify
releases or tags with `gh`.

### 0. Once per machine

- `pip install -r tools/docsync/requirements.txt`, Docker, `jq`, `yarn install`.
- `gh auth login` with an account that can **see** draft releases of
  `dragonflydb/dragonfly`.
  - `gh` is used read-only: step 1 runs `gh release list`/`gh release view`, and
    `build_prerelease_image.sh` runs `gh api` and `gh release download`.
  - GitHub shows a draft release only to accounts with write permission on
    the repository. That is a visibility rule only: nothing is ever written.
    Any other account gets `release not found` for a draft.
- `export OPENAI_API_KEY=...` for the LLM steps (ACL repair, flags polish,
  `docs_sync.py`). `compat_sync.py` does not need it.
- The offline unit tests must pass (pytest is not required):

  ```sh
  python3 -m unittest discover -s tools/docsync -t . -p 'test_*.py'
  ```

### 1. Choose the versions and the image source

`OLD` and `REDIS` are recorded in the `Verification:` line at the end of the
compatibility page. Read it now, because step 5 rewrites it:

```sh
grep '^Verification:' docs/command-reference/compatibility.md
```

For `Verification: Dragonfly v2.0.0; Redis 8.6.4; ...`, set `OLD` to the
Dragonfly value and `REDIS` to the Redis value. Change `REDIS` only when you
want to compare against a newer Redis. `NEW` is the release to document.

`NEW` is always the Docker image and git tag (`v2.1.0`). The facts file, the
branch and the `Verification:` line are named after it. The GitHub release can
have a different tag: the v2.1.0 image was shipped by the release `v2.1`, so
`gh release view v2.1.0` answers `release not found`. Find the release with
`gh release list`, and test whether the image is published with
`docker manifest inspect`:

```sh
NEW=v2.1.0
OLD=v2.0.0
REDIS=8.6.4
git switch -c docs/sync-$NEW
gh api repos/dragonflydb/dragonfly/git/ref/tags/$NEW --jq .object.sha
gh release list -R dragonflydb/dragonfly --limit 3
docker manifest inspect docker.dragonflydb.io/dragonflydb/dragonfly:$NEW >/dev/null && echo published
```

- **Published image:** run
  `docker pull docker.dragonflydb.io/dragonflydb/dragonfly:$NEW`, then `PULL=`.
- **Draft release** (no image yet; `gh release view <release tag> --json isDraft`
  says `true`): see [Unreleased tags](#unreleased-tags-draft-github-release).
  1. Run `RELEASE_TAG=<release tag> tools/docsync/build_prerelease_image.sh $NEW`
     (`RELEASE_TAG` defaults to `$NEW`). The last line must be
     `OK: ... (binary sha256 ... == release asset)`.
  2. Set `PULL=--skip-pull`.

### 2. Capture facts

```sh
python3 tools/docsync/dfly_facts.py --tag $NEW $PULL
```

The script prints `dragonfly <version>-<commit>` and writes
`tools/generated/facts/$NEW.json`. The version label can differ from the tag
(`v2.1` for the tag `v2.1.0`); only the commit is checked against the tag.
Steps 3, 4 and 6 reuse that file; step 5 does not read it. It stops if the
image was not built from the tag's commit.

### 2b. Pages for new commands and features

No script creates pages: `acl_sync.py` and `docs_sync.py` only edit pages that
exist. Write pages for new commands and features by hand before step 3, and
commit them.

- The H1 of a command page is the command name (`# CLIENT TRACKINGINFO`).
  Both scripts key on it.
- `acl_sync.py --dry-run` (step 3) lists the `ACL CAT entries used by no page`:
  server commands that have no page yet. For a new page, its `UPDATE FAILED`
  entry prints the exact ACL line to add.
- Leave hand-written pages out of the step 6 plan, or review their examples
  after it.

### 3. ACL category lines: `acl_sync.py`

```sh
python3 tools/docsync/acl_sync.py --tag $NEW $PULL --dry-run
python3 tools/docsync/acl_sync.py --tag $NEW $PULL
git diff docs/command-reference docs/managing-dragonfly/acl-categories.md
```

- The `--dry-run` run is a preview: no pages written, no OpenAI. It still runs
  the live check, which starts a container from the `$NEW` image.
- Nothing is written unless all of these pass:
  - **facts shape checks** (exit 4): the facts must match the model in
    `acl_model.py`, e.g. no unknown hidden command, no COMMAND entry without a
    category. A violation means Dragonfly changed how it reports ACLs: update
    `acl_model.py`, never the pages by hand;
  - **live check** (exit 3): `ACL DRYRUN` on a container from the facts image must
    allow each page's command for exactly the categories acl_sync resolved, and
    name the same governing entry. `--no-verify-live` skips it;
  - **categories page** (exit 1): `docs/managing-dragonfly/acl-categories.md`
    exists, has its markers, and every category has a description.
- Check the `Updated` list (each line is tagged `[own]`, `[acl-only CLIENT KILL]`,
  `[inherited from XINFO]` or `[routed -> _XGROUP_HELP]`), `not synced`,
  `ACL CAT entries used by no page`, the duplicate-page list and `UPDATE FAILED`.
- A page under `UPDATE FAILED` (exit code 1) needs a manual fix. Its
  `expected:` line shows the exact ACL line to use: add it if the page has
  none, or keep one ACL line if the page has several. An `unrecognised ACL line`
  is never sent to the LLM: rewrite it as `**ACL categories:** ...`.
- The run also regenerates the command lists in
  `docs/managing-dragonfly/acl-categories.md`. A category without a description
  fails the run: add it to `CATEGORY_DESCRIPTIONS` in `acl_sync.py`.
- Commit.
- This step runs before step 6 because `docs_sync.py` refuses to change ACL
  lines.

### 4. Flags page: `flags_sync.py`

```sh
python3 tools/docsync/flags_sync.py --tag $NEW --previous-tag $OLD $PULL --dry-run
python3 tools/docsync/flags_sync.py --tag $NEW --previous-tag $OLD $PULL
git diff docs/managing-dragonfly/flags.md
```

- `--previous-tag $OLD` loads the facts of the release the page documents now
  (it pulls that image if needed). The LLM may then update the sections of
  flags whose `--helpfull` text changed since `$OLD`, listed under
  `Documented flags whose --helpfull text changed`. Without it, only new flags
  and enum tables are written, and the run says help-text changes were not checked.
- The page is rebuilt from the mechanical result: only new flags, those
  changed-help sections and enum tables come from the LLM. Any other section the
  LLM rewrote is kept as it was, and the run lists it under
  `kept the page's text for N section(s)`.

- The `--dry-run` run is the mechanical report: flags.md is not written and
  OpenAI is not called.
- Check the removed sections (flags the server no longer reports), the new
  flags and the changed defaults.
- The `LLM polish:` line should say `applied`. After `VALIDATION FAILED` or
  `skipped (...)`, only the mechanical result is on disk. The raw output of a
  rejected polish is in `tools/generated/llm_debug/`.
- Exit codes:
  - **1:** new flags were not added ("Flags missing from doc, NOT added"), or
    a documented flag has no `default:` line ("Default-fix FAILURES").
    `--dry-run` therefore exits 1 whenever there are new flags.
  - **2:** the facts could not be loaded.
- Commit.

### 5. Compatibility table: `compat_sync.py`

```sh
python3 tools/docsync/compat_sync.py --dragonfly-ref $NEW --redis-ref $REDIS
python3 tools/docsync/compat_sync.py --dragonfly-ref $NEW --redis-ref $REDIS --write-table
git diff docs/command-reference/compatibility.md
```

- Before the second command, review
  `tools/generated/compatibility/<ts>/tasks.json` and `draft_table.md`. In
  `tasks.json`, check:
  - `status-change-applied`: entries with `replaced_details` replaced a
    curated note;
  - `missing-row`;
  - `unresolved-command`.
- `--write-table` writes the page only for a full run: no `--filter`, no
  `--limit`.
- Commit.

### 6. Page content: `docs_sync.py`

```sh
python3 tools/docsync/docs_sync.py --before $OLD --after $NEW $PULL --dry-run
python3 tools/docsync/docs_sync.py --before $OLD --after $NEW --discover-only
python3 tools/docsync/docs_sync.py --update-only-from tools/generated/update_plans/plan_<ts>.json $PULL
git diff docs/
```

1. **`--dry-run`** checks the tags, the image and the facts. It makes no
   OpenAI call and writes no pages, plan or results.
2. **`--discover-only`** makes one LLM call and prints
   `plan saved: tools/generated/update_plans/plan_<ts>.json`.
   - Review that plan and delete the entries you do not want.
   - To add a page, append `{"path": "docs/...md", "reason": "manual"}` to
     `files_to_update`.
   - Alternatively, pass `--also-update <file>` to the discover command: one
     repo-relative path per line, e.g. `docs/command-reference/strings/incr.md`.
     Re-running discover makes a new triage and a new plan.
   - `flags.md` and `compatibility.md` are never planned or edited: steps 4
     and 5 own them.
3. **`--update-only-from`** updates the pages in the plan. To update in
   batches, add `--filter 'docs/command-reference/strings/*'`.
4. **Results:** read `tools/generated/update_plans/results_<ts>.json` and fix
   the `failed`/`error` entries. Rejected LLM output is in
   `tools/generated/llm_debug/`.
5. **Examples:** review every changed example block by hand.
   - Only `dragonfly> ` lines in changed or new ```` ```shell ```` blocks are
     run in Docker and get their output replaced. Each block runs in one
     redis-cli session after `FLUSHALL`, so HELLO 3, SELECT, MULTI and AUTH
     carry over inside the block, but keys never carry into the next block.
     An example that depends on an earlier block's keys gets the wrong output.
   - A page whose LLM output changes the front matter, or removes or changes an
     existing `dragonfly>` command or `$ redis-cli` line in any code block, is
     rejected and not written:
     an example that fails on its own needs setup lines, not removal.
   - Existing prose that the LLM removed or rewrote is listed in the run summary
     and in `removed_text` in the results. Keep a change only if the old line was
     wrong for the new release.
   - Server error replies are written into the page, because a documented
     error case is legitimate. Every one of them is listed in the run summary
     and in `example_errors` in the results: check each against the page text.
   - A changed block that times out (30 s), loses its connection, writes to
     redis-cli's stderr, or contains QUIT/EXIT fails the page; the page is not
     written and the LLM markdown is saved as
     `tools/generated/llm_debug/docs_sync_unverified_*.md`.
   - Blocks with `$ redis-cli ` lines, and blocks with replication, cluster,
     SUBSCRIBE or MONITOR commands, are not run: their output stays as the LLM
     wrote it. New or changed blocks of that kind are listed under
     `unverified_blocks`: verify them by hand.
6. Commit.

### 7. Build

```sh
yarn build
```

The result is the local branch with one commit per step. Publishing it is a
separate decision and is not part of this runbook.

### If the tag moves while the release is a draft

A script stops with one of these messages:
- "image ... was built from X, but tag ... points to Y upstream";
- "inputs are from different commits";
- "plan was discovered at ...".

To recover:

1. Wait until upstream has rebuilt the release assets for the new commit.
   `build_prerelease_image.sh` refuses assets built from the old commit.
2. Re-run `tools/docsync/build_prerelease_image.sh $NEW`.
3. Re-run steps 2–5. Stale caches are re-captured automatically.
4. Re-run step 6 from `--discover-only`; the old plan is refused.

### After the release is published

Upstream's "Docker Release-v2" workflow pushes the image only after the
release is published, so the image cannot be pulled for a while. Keep the
local build until the pull works: `docker pull` replaces it.

1. Check that the official image exists. If this fails, wait for the workflow
   and retry:

   ```sh
   docker manifest inspect docker.dragonflydb.io/dragonflydb/dragonfly:$NEW
   ```

2. Pull the image and re-capture the facts:

   ```sh
   docker pull docker.dragonflydb.io/dragonflydb/dragonfly:$NEW
   jq -S .data tools/generated/facts/$NEW.json | sha256sum
   python3 tools/docsync/dfly_facts.py --tag $NEW
   jq -S .data tools/generated/facts/$NEW.json | sha256sum
   jq .meta.image_local_build tools/generated/facts/$NEW.json
   ```

3. Compare the output. The first hash is the draft build; the second and the
   `false` are the official image. The official image is built from the same
   commit, so the two hashes should match. If they differ, re-run steps 3–6
   without `--skip-pull`.

## Tags, commits and unreleased versions

Every script keys its inputs by tag name, but a tag is only a pointer: while a
GitHub release is still a draft, upstream may force-move its tag. So the scripts
resolve the tag to a commit and require all inputs to agree on it
(`dfly_refs.py`):

- **Source checkout** (`/tmp/dragonfly-docsync`): `docs_sync.py`, and
  `flags_sync.py` when it re-parses the source, compare the tag with upstream
  before checking it out. If the tag is new or moved upstream, they fetch tags
  with `--force --prune-tags`. The tag must then match upstream. A tag that no
  longer exists upstream, cannot be resolved or cannot be checked out is an
  error; previously the old tree was silently used. So is a checkout with local
  changes or untracked files, since they would be parsed as part of the tag.
  Only tags are accepted; `docs_sync --before` also takes a local revision that
  is not a tag. `compat_sync.py` has its own checkout logic (see its section):
  it also re-fetches a cached tag that moved and rejects a cached tag that was
  deleted upstream, but accepts branches and SHAs.
- **Docker image**: its commit is read from `dragonfly --version`.
  `dfly_facts.py` refuses to capture from an image whose commit differs from the
  tag's upstream commit, and refuses a tag that does not exist upstream. Docker never pulls implicitly (`--pull=never`), so with
  `--skip-pull` the image must already exist locally.
- **Cached facts** (`facts/<tag>.json`) record `meta.dragonfly_commit`. A cached
  file whose commit differs from the tag's upstream commit, or from the local
  image, or whose tag no longer exists upstream, is re-captured automatically. The same applies to a file written before
  commit tracking existed. The flags_sync source cache (`source/<tag>.json`)
  works the same way.
- `docs_sync.py` plans record `before_commit`/`after_commit`. Phase 2 stops
  before touching any page in these cases: either commit is no longer what its
  tag points to (re-run discover); the source, image and facts commits differ;
  or the image has no build SHA.

The upstream check uses `git ls-remote` against GitHub (30s timeout; a fetch
is bounded to 300s). When GitHub cannot be reached, the scripts print one
WARNING per host and fall back to the local checkout/image only. They do not
silently skip the check.

### Unreleased tags (draft GitHub release)

Upstream pushes `docker.dragonflydb.io/dragonflydb/dragonfly:<tag>` only when the
release is **published**. While it is a draft, `docker pull` fails with
`not found`/`manifest unknown`. Build the image from the draft release assets
instead. The
binary is byte-identical to the one the release will ship:

```sh
tools/docsync/build_prerelease_image.sh v2.0.0      # needs gh with access to the draft
RELEASE_TAG=v2.1 tools/docsync/build_prerelease_image.sh v2.1.0   # release tag != image tag
```

Then pass `--skip-pull` to every script (`dfly_facts.py`, `acl_sync.py`,
`flags_sync.py`, `docs_sync.py`). If the tag moves again, the scripts stop with
"image ... was built from X, but tag ... points to Y upstream", "inputs are from
different commits", or "plan was discovered at ...". Wait for upstream to rebuild
the release assets (the build script refuses assets from the old commit),
re-run the build script, then re-run the scripts. Once the release is published, remove the local image
(`docker rmi ...:v2.0.0`) and run without `--skip-pull`. The official image has
the same commit, so cached facts stay valid.

## acl_sync.py

Updates the `**ACL categories:**` line on every published command-reference page
whose H1 is a server command, and the command lists of
`docs/managing-dragonfly/acl-categories.md`. Pages Docusaurus does not publish
(a path component starting with `_`, e.g. `pubsub/_unsupported/`) are skipped.

**Which categories a page shows.** The categories of the entry Dragonfly checks
when a client sends the page's H1 as a command (`acl_model.resolve`, which follows
`CommandRegistry::FindExtended` and `CommandId::AclTarget`; verified against
`ACL DRYRUN` on every page of a live v2.1.0 server). Only the first two words of
the H1 count; further words are arguments.

- **own:** the H1 is an entry of its own: a command listed by `COMMAND`, a hidden
  command (`DFLYCLUSTER`), or an ACL subcommand (`ACL SETUSER` is registered as a
  separate command). `+acl` and `-acl` change only the bare `ACL` command.
- **acl-only:** `ACL CAT` lists `CMD|SUB` but `COMMAND` does not list `CMD SUB`.
  In v2.1.0: `CLIENT KILL/LIST/MIGRATE/PAUSE/UNPAUSE` and
  `MEMORY ARENA/DECOMMIT/DEFRAGMENT/DEFRAGMENT-SEGMENTS/TRACK`. The container runs
  it, but the server checks the subcommand's own categories. `+cmd` grants it,
  `+cmd|sub` grants only it, and removing one of its categories denies only it.
- **inherited:** `CMD SUB` is not an entry, so the server checks the container's
  entry. No `cmd|sub` rule exists for it (`+client|getname` is rejected).
  Inheriting does not prove that `SUB` exists.
- **routed:** `XGROUP HELP` alone runs the hidden `_XGROUP_HELP` command
  (`acl_model.ROUTED_SUBCOMMANDS`). `+xgroup` does not grant it.
- `ACL <SUB>` never falls back to `ACL`: an unknown ACL subcommand is not a
  server command.

Since v2.1.0 `ACL CAT` spells subcommand entries `CMD|SUB` (`ACL|SETUSER`); older
releases spelled them `ACL SETUSER`. `tools/generated/facts/<tag>.json` keeps the
spelling `ACL CAT` returns, and `acl_model.command_acl_view` reads both.

**Order of a run.** Nothing is written before the last step, so exit codes 3 and
4, and a categories page that cannot be generated, never leave a half-updated tree.

1. **Facts shape checks** (`acl_model.invariants`, exit 4): every entry name is
   `CMD` or `CMD SUB`; an entry missing from `COMMAND` is an ACL-only subcommand
   of a listed parent or one of `KNOWN_HIDDEN`; every `COMMAND` entry has
   categories; the routed target exists; the facts have the `ACL CAT` member
   lists, and they name the same entries as `command_acl`. These checks would
   have stopped the v2.1.0 run that read `ACL|SETUSER` as an unknown command.
2. **Mechanical pass** — minimal-diff edits, computed for every page:
   - if the *set* of categories on a page already equals the server set,
     the file is **not touched at all**, even if the line is spelled oddly;
   - when the set differs, categories that stay keep their original
     order, new ones are appended (alphabetically), removed ones are
     dropped. A label with a qualifier
     (`**ACL categories (Dragonfly v2.0.2):**`) is rewritten as
     `**ACL categories:**`;
   - an ACL-like line the parser cannot read is a failure that is never sent
     to the LLM.
3. **Live check** (exit 3; `--no-verify-live` skips it): a container from the
   facts image (its commit must equal the facts commit) gets one user per
   `ACL CAT` category (`ON nopass ~* &* -@all +@<category>`) plus `+@all` and
   `-@all` users. For every page H1, `ACL DRYRUN <user> <H1 words>` (no further
   arguments: `XGROUP HELP <arg>` would not be routed) must allow exactly the
   resolved categories, and the `-@all` user's denial must name the resolved
   entry. A page resolved as "not a server command" must be unknown to the server.
4. **Categories page check** (exit 1, nothing written): the page exists, has
   its markers, and every category has a description in `CATEGORY_DESCRIPTIONS`.
   It runs before the LLM repair, so a run that cannot finish makes no LLM calls.
5. **LLM repair pass** (requires `OPENAI_API_KEY`; skipped by `--no-llm` and
   `--dry-run`) — for pages with no ACL line or several ACL lines. Container
   pages ("This is a container command for ...") carry the command's ACL line on
   this site (CONFIG, MEMORY, SLOWLOG, SCRIPT), so one without it is repaired like
   any other page. The patch is accepted only if its diff inserts one ACL line
   (plus at most two blank lines) and deletes only ACL-like lines, and the page
   ends with exactly one ACL line with the server's categories. A page the model
   calls "not a page for this command" is listed for confirmation and the run
   exits 1.
6. **Write** the updated pages and the categories page (not with `--dry-run`).

The report lists every page that was not synced, the `ACL CAT` entries no page
uses (candidates for new pages; not shown with `--filter`), commands documented
on more than one page, and the failures with the exact expected line.

```sh
python tools/docsync/acl_sync.py --tag v2.1.0
python tools/docsync/acl_sync.py --tag v2.1.0 --dry-run          # pages not written, no OpenAI
python tools/docsync/acl_sync.py --tag v2.1.0 --no-llm           # mechanical-only
python tools/docsync/acl_sync.py --tag v2.1.0 --filter "search/*"
python tools/docsync/acl_sync.py --facts tools/generated/facts/v2.1.0.json
python tools/docsync/acl_sync.py --tag v2.1.0 --no-verify-live   # no container
```

Exit codes: 0 ok; 1 pages failed or need confirmation; 2 facts could not be
loaded or an unexpected error; 3 live check failed; 4 facts shape check failed.

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
`--add-missing-rows`). Curated Details text is kept while the verdict agrees
with it. That covers a free-text note on a row whose label did not change ("Use
MEMORY DECOMMIT instead."). It also covers human wording around the same
`Missing:` options ("Missing: SAMPLES, which is accepted but ignored."), as
long as the wording names no other option of the command. Only upper-case
keywords (`DIFF1`, `MALLOC-STATS`) in a `Missing:` list count as options, and a
`Missing:` list on a non-partial row is never kept. When the label or the missing options
change, the derived text replaces the note, and the change log entry carries
`replaced_details` so the lost note can be reviewed. Writing the doc is
**opt-in** (`--write-table`); by
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
   `"COMMAND DOCS Not Implemented"` — recognized but stubbed), and **not** when
   it is only an argument of a reply-builder call: `rb->SendBulkString("redirect")`
   is the CLIENT TRACKINGINFO reply field, not CLIENT TRACKING parsing a
   `REDIRECT` option. Matching stays case-insensitive: a case-sensitive match
   would drop lowercase literals the parsers do compare (geo units, aggregate
   function names, `JSON.DEBUG memory`). Any genuinely
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
stale cache, or a cached tag has moved upstream, the tool fetches tags (with
`--force`) and retries automatically. Use `--refresh-source` to fetch before
every checkout. The Dragonfly commit is recorded in `metadata.json`, suffixed
`-dirty` if `src/` has uncommitted changes. With `--dragonfly-source-dir`,
`--dragonfly-ref` must match that directory's HEAD. The directory must be the
root of its own git checkout to be verified; otherwise a WARNING is printed.
`--write-table` together with `--dragonfly-ref` is refused when that checkout
has uncommitted changes under `src/`.

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
     When a flag is declared more than once (test and benchmark binaries
     redeclare `force_epoll`, `tcp_nodelay`), the declaration from the file
     that `--helpfull` names as the flag's group is used.
     Cached in `tools/generated/source/<tag>.json` together with the
     commit it was parsed at. The cache is re-parsed when that commit no
     longer matches the facts, and the checkout must match the facts'
     commit. Only loaded when the LLM polish runs.

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
     for adding the enum-value table to the description. A section with a
     line that already maps the integer to the constant, such as
     ``- `3` — `MULTI_ENTRY_LZ4` ``, is left as it is.

3. **LLM polish** (requires `OPENAI_API_KEY`; runs only when there is something
   for it to write). The OpenAI model receives the mechanically-fixed page, the
   ground-truth dict, the source-facts dict (with C++ comments and enum tables),
   the flags to add, the documented flags whose `--helpfull` text changed since
   `--previous-tag` (`flags_to_update`, with the old and new help), and the enum
   defaults to expand. It:
   - writes descriptions for flags missing from the doc using the help
     text + source comments;
   - updates the sections in `flags_to_update` to the new help text;
   - for enum-typed defaults, keeps the integer in `default:` and adds a
     value table to the description body.
   **Deterministic merge:** the page is then rebuilt from the mechanical result,
   taking from the model's output only those sections; a new flag goes after the
   section that precedes it there. Every other byte, including the intro and the
   sections the model reworded anyway, stays as the mechanical pass left it.
   On the v2.1.0 run the model reworded 183 unchanged sections despite the prompt;
   the merge discards exactly those edits.
   The LLM output is validated (every server flag present, defaults match
   modulo byte equivalence, enum defaults still integers). If validation
   fails the LLM output is discarded and the mechanical-only result stays
   on disk. The raw response is saved under `tools/generated/llm_debug/`
   for inspection.

Upstream `glog-src/` and `abseil_cpp-src/` flags are filtered out of
auto-add (but their defaults are still corrected if a human chose to
document them).

```sh
python tools/docsync/flags_sync.py --tag v2.1.0 --previous-tag v2.0.0
python tools/docsync/flags_sync.py --tag v1.38.0
python tools/docsync/flags_sync.py --tag v1.38.0 --dry-run       # mechanical report, page not written, no OpenAI
python tools/docsync/flags_sync.py --tag v1.38.0 --no-llm        # mechanical only
python tools/docsync/flags_sync.py --tag v1.38.0 --skip-source   # no C++ context
python tools/docsync/flags_sync.py --tag v1.38.0 --refresh-source  # re-parse even if current
python tools/docsync/flags_sync.py --facts tools/generated/facts/v1.38.0.json
```

Flags that the doc still lists but the server no longer reports are
**deleted** during the mechanical pass and listed in the run summary so
the change is visible. The server is the authoritative source — if a
flag isn't reported, documenting it would mislead users.

## docs_sync.py

Updates documentation pages whose content drifted between two Dragonfly
releases. It never plans or edits `docs/managing-dragonfly/flags.md` or
`docs/command-reference/compatibility.md`; `flags_sync.py` and `compat_sync.py`
own them. Plan paths, whether from discovery, `--also-update` or a hand-edited
plan, are normalized first, and paths outside `docs/` are rejected. Two phases
driven by one command:

1. **Discover** (single LLM call). Computes the Dragonfly source diff
   between `--before` and `--after` (every commit subject + every changed
   file with added/deleted line counts, `src/` first, never the raw diff),
   walks every published `.md` under `docs/` (a path part starting with `_`,
   such as `pubsub/_unsupported/`, is skipped and never planned), and asks
   OpenAI which pages plausibly
   need updating and why. It aborts if either tag cannot be resolved, or
   if the range has no commits and no `--also-update` pages were given. The plan is saved to
   `tools/generated/update_plans/plan_<ts>.json`.

   An optional `--also-update FILE` adds explicit paths to the plan
   regardless of LLM judgement (one path per line, comments with `#`
   ignored). These are **forced overrides** — they are always processed
   even if the LLM decided no change is needed.

2. **Update** (one LLM session per file). For each file in the plan:
   - Read the current page.
   - Identify the topic from the H1; if it matches a real server command,
     pull the C++ handler body from the Dragonfly checkout at `--after`
     and the `COMMAND` data captured by `dfly_facts.py`. Pages under
     `docs/command-reference/` also get the ACL categories the server checks
     for the command (`acl_model.resolve`), as information only.
   - Boot a Dragonfly container at `--after` (with `--cluster_mode=emulated`
     for cluster-family commands). The image is pulled once per run, unless
     `--skip-pull` is given, and checked against the source and facts
     commits before any page is processed. If the container fails to boot
     for a page, that page is marked `failed` and left untouched. It is not
     rewritten with unverified example output. Every `docker` call has a
     timeout (a block runs under `timeout 30` inside the container), and the
     container is removed even when a step fails. A page without examples
     gets a container too when the LLM adds some.
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
       * **do NOT modify, remove or add a `**ACL categor(y|ies)...:**`
         line** (a qualified label counts) — that metadata is owned by
         `acl_sync.py` and must stay byte-identical;
       * **do NOT change page structure** — keep every existing section
         in place, do not add new top-level sections, do not move or
         append example blocks. New examples must be placed inside the
         page's existing `## Examples` section, beside related ones;
       * never write a bare `<placeholder>` outside a fenced code block.
   - **Structural validation** runs first. Catches catastrophic LLM
     failures: output shorter than 80 non-whitespace chars, output
     shrunk to less than half of input, output that's just `...`,
     missing frontmatter / H1 / `<PageTitle>` / `import PageTitle`,
     dropped H2 sections, a changed front matter, a removed or changed existing
     `dragonfly>` example command or `$ redis-cli` line, a modified, removed or
     added ACL line, and a
     changed topology or SUBSCRIBE/MONITOR block. On any failure the run is
     marked `failed`, the raw LLM markdown is saved to
     `tools/generated/llm_debug/docs_sync_rejected_<file>_<ts>.md`, and
     the file on disk is **not touched**.
   - **Docker verification**: every changed or new ```` ```shell ```` block
     with `dragonfly>` lines runs in **one redis-cli session**
     (`docker exec -i <container> timeout 30 redis-cli --no-raw`) after
     `FLUSHALL`, and its replies replace the output the LLM wrote:
       * command lines are sent as written: redis-cli parses quotes and `\x`
         escapes itself;
       * replies are split by an unknown-command marker
         (`__DOCSYNC_SEP_<n>__`) sent after each command, except between
         MULTI and EXEC/DISCARD/RESET, where each queued command answers one
         line. The markers count as commands and unknown-command errors in
         INFO/CLIENT INFO counters;
       * connection state (HELLO 3, SELECT, MULTI, AUTH, CLIENT TRACKING)
         carries within a block; keys do not carry across blocks, while ACL
         users, CONFIG values and scripts do, in page order;
       * changed blocks run on a fresh container, after the unchanged blocks
         before them are replayed in page order (their text is kept);
       * redis-cli's `(N.NNs)` timing lines are dropped, so output matches
         one-shot calls; blank and `#` comment lines that end a command's
         predicted output are kept;
       * `(error)` replies are written (a documented error case is
         legitimate) and recorded in `example_errors`;
       * a timeout, a lost connection, anything on redis-cli's stderr, a
         refused FLUSHALL or MULTI, or QUIT/EXIT fails the page: it is not
         written, and the LLM markdown is saved as
         `tools/generated/llm_debug/docs_sync_unverified_<file>_<ts>.md`;
       * blocks with `$ redis-cli` lines, blocks with SUBSCRIBE, PSUBSCRIBE,
         SSUBSCRIBE or MONITOR, and topology-dependent blocks are kept as
         written; new or changed ones are listed in `unverified_blocks`.
     The LLM is encouraged to extend examples with setup commands at the top
     of a block (e.g. `RPUSH mylist a b c` before `LRANGE mylist 0 -1`) when
     this makes the example clearer.
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
    --filter "docs/command-reference/strings/*"
python tools/docsync/docs_sync.py --before v1.37.0 --after v1.38.0 --dry-run
    # checks tags/image/facts, lists the planned pages (only --also-update ones,
    # since triage is not run); no OpenAI, no pages/plan/results written
```

`--dry-run` never calls OpenAI and never writes doc pages, plans or results in
any script. It may still refresh caches the checks need: capture
`tools/generated/facts/<tag>.json`, check out the Dragonfly source, pull the
image. To preview real LLM edits, run without it on a branch and review
`git diff docs/`.

Per-file results are written to
`tools/generated/update_plans/results_<ts>.json`. Each entry has a
status (`updated`, `unchanged`, `failed`, `skipped`, `missing`, `error`)
and a `notes` list with everything the run noticed: which sibling style
was used, whether `diff_context` was present, how many invocations were
verified in Docker, blocks that did not complete, whether MDX safety wrapped
anything, why a write was skipped. `example_errors` lists every `(error)`
reply written into an example (`{block, command, reply}`) and
`unverified_blocks` the new blocks that were kept as written, and `removed_text`
the existing prose lines the output no longer contains; the run summary prints
all three. Failed entries also point at the saved raw LLM output under
`tools/generated/llm_debug/` so the failure mode can be inspected without
re-running the LLM.

## dfly_facts.py (helper)

Boots `docker.dragonflydb.io/dragonflydb/dragonfly:<tag>`, captures
`COMMAND`, `ACL CAT`, `INFO`, `CONFIG GET *` and parses
`dragonfly --helpfull`, then writes a JSON snapshot under
`tools/generated/facts/<tag>.json`.

Sync scripts call this on demand and reuse the cached file while its
`meta.dragonfly_commit` still matches the tag (see "Tags, commits and
unreleased versions"). The capture aborts if the image was built from a
different commit than the tag, if `dragonfly --version` carries no build SHA,
or if `--helpfull` yields no flags. `meta` also
records `dragonfly_version`, `image_id` and `image_local_build`. It can also be
run by hand:

```sh
python tools/docsync/dfly_facts.py --tag v1.38.0
python tools/docsync/dfly_facts.py --tag v1.38.0 --skip-pull
```

The `data` portion of the output is bit-stable across runs on the same
tag (`jq -S .data <out>.json | sha256sum` is identical between runs).
The `meta` portion is volatile by design (timestamp, host-dependent
runtime config).
