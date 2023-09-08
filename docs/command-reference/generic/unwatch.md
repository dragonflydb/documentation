---
description: Forget about all watched keys
---

# UNWATCH

## Syntax

    UNWATCH 

**Time complexity:** O(1)

**ACL categories:** @fast, @transaction

Flushes all the previously watched keys for a [transaction][tt].

[tt]: https://redis.io/topics/transactions

If you call `EXEC` or `DISCARD`, there's no need to manually call `UNWATCH`.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): always `OK`.
