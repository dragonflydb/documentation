---
description:  Discover how to use Redis SLOWLOG LEN command to retrieve the current number of entries in the slow log.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG LEN

<PageTitle title="Redis SLOWLOG LEN Command (Documentation) | Dragonfly" />

## Syntax

    SLOWLOG LEN

The `SLOWLOG LEN` returns the current number of entries in the slow log.
A new entry is added to the slow log whenever a command exceeds the execution time threshold defined by the `slowlog_log_slower_than` configuration directive.
The maximum number of entries in the slow log is governed by the `slowlog_max_len` configuration directive.
Once the slog log reaches its maximal size, the oldest entry is removed whenever a new entry is created.
The slow log can be cleared with the `SLOWLOG RESET` command.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): The number of entries in the slow log.
