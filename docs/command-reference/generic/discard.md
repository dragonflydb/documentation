---
description: "Master Redis DISCARD command that discards all commands issued after MULTI."
---

import PageTitle from '@site/src/components/PageTitle';

# DISCARD

<PageTitle title="Redis DISCARD Command (Documentation) | Dragonfly" />

## Syntax

    DISCARD

**Time complexity:** O(N), when N is the number of queued commands

**ACL categories:** @fast, @transaction

Flushes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: https://redis.io/topics/transactions

If `WATCH` was used, `DISCARD` unwatches all keys watched by the connection.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): always `OK`.
