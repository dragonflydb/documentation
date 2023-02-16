---
description: Discard all commands issued after MULTI
---

# DISCARD

## Syntax

    DISCARD 

**Time complexity:** O(N), when N is the number of queued commands

Flushes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: https://redis.io/topics/transactions

If `WATCH` was used, `DISCARD` unwatches all keys watched by the connection.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): always `OK`.
