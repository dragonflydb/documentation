#!/usr/bin/env bash
#
# Check external links in the docs with lychee, and retry links that fail for transient reasons.
#
# lychee itself retries only timeouts and some dropped connections. It fails at once on refused
# connections, DNS, TLS and HTTP/2 errors, and HTTP 5xx responses, which in CI are usually
# transient. When links fail like that, this script runs lychee again, up to LINK_CHECK_ATTEMPTS
# runs in total, until every link passes. lychee reuses passing (2xx) results from its cache and
# never caches failures, so a new run requests only the links that still fail, plus the few links
# accepted with another status, such as 403.
#
# When a link returns an HTTP 4xx other than 408 or 429, such as 404, the script stops and fails
# without retrying anything. A retry could hide a broken link behind a 403 or 429 from a bot wall,
# which .lychee.toml accepts. The cost is that a transient 4xx, such as a site outage that returns
# 404 for every page, also fails the check.
#
# Run it from the repository root, with lychee on PATH:
#   .github/scripts/check-external-links.sh 'docs/**/*.md'
#   .github/scripts/check-external-links.sh docs/integrations/clickhouse.md
#
# Environment:
#   LINK_CHECK_ATTEMPTS  Maximum number of lychee runs. Default: 10.
#   LINK_CHECK_DELAY     Seconds to wait before the first retry. Each later wait is twice as
#                        long, up to 30 seconds. Default: 5.
#   GITHUB_TOKEN         Used by lychee for github.com links.
#   GITHUB_STEP_SUMMARY  Set by GitHub Actions. The final report is appended to it.
#
# Exit status: 0 if all links pass, 2 if some links are broken or still fail on the last run,
# or lychee's own exit status if lychee itself fails.

set -uo pipefail

attempts="${LINK_CHECK_ATTEMPTS:-10}"
pause="${LINK_CHECK_DELAY:-5}"
max_pause=30

if [[ ! "$attempts" =~ ^[1-9][0-9]*$ ]]; then
  echo "LINK_CHECK_ATTEMPTS must be a positive integer, got '$attempts'." >&2
  exit 1
fi
if [[ ! "$pause" =~ ^(0|[1-9][0-9]*)$ ]]; then
  echo "LINK_CHECK_DELAY must be a whole number of seconds, got '$pause'." >&2
  exit 1
fi
if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <file or glob>..." >&2
  exit 1
fi

report="$(mktemp)" || exit 1
trap 'rm -f "$report"' EXIT

# lychee lists each failed link in its report as "* [<status>] <url> ...", where <status> is
# an HTTP status code, ERROR (such as a refused connection) or TIMEOUT.
has_broken_links() {
  awk 'BEGIN { found = 0 } /^\* \[4[0-9][0-9]] </ && !/^\* \[(408|429)] </ { found = 1 } END { exit !found }' "$report"
}

for ((attempt = 1; ; attempt++)); do
  args=(--config .lychee.toml --root-dir "$PWD" --cache --no-progress --format markdown --output "$report")
  if ((attempt > 1)); then
    # The first run uses lychee's own retries from .lychee.toml, like a plain lychee run.
    # Later runs make one request per link, because this loop does the retrying.
    args+=(--max-retries 0)
  fi

  # Do not show a previous run's report if lychee fails before writing one.
  : >"$report"
  status=0
  lychee "${args[@]}" -- "$@" || status=$?

  # Exit status 2 with no report is a lychee command-line error, not a link failure.
  if ((status != 2)) || [ ! -s "$report" ] || has_broken_links || ((attempt >= attempts)); then
    break
  fi

  if ((pause > max_pause)); then
    pause=$max_pause
  fi
  echo "::group::Attempt $attempt of $attempts: some links failed, retrying them in ${pause}s"
  cat "$report"
  echo "::endgroup::"
  sleep "$pause"
  pause=$((pause * 2))
done

echo "Attempt $attempt of $attempts:"
cat "$report"

note=""
if ((status == 0)); then
  if ((attempt > 1)); then
    note="All links passed on attempt $attempt of $attempts. The links that failed on earlier attempts are listed in the log."
    echo "::notice::$note"
  fi
elif ((status == 2)) && [ ! -s "$report" ]; then
  note="lychee exited with status 2 before checking any links. See the error above."
  echo "::error::$note"
elif ((status == 2)) && has_broken_links; then
  note="Some links returned an HTTP 4xx error, so the check stopped without retrying. Other failures in the report may be transient."
  echo "::error::$note"
elif ((status == 2)); then
  note="Some links still failed on the last attempt ($attempt of $attempts)."
  echo "::error::$note"
else
  note="lychee exited with status $status."
  echo "::error::$note"
fi

if [ -n "${GITHUB_STEP_SUMMARY:-}" ]; then
  {
    cat "$report"
    if [ -n "$note" ]; then
      printf '\n%s\n' "$note"
    fi
  } >>"$GITHUB_STEP_SUMMARY"
fi
exit "$status"
