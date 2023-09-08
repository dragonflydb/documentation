---
description: Mark the start of a transaction block
---

# MULTI

## Syntax

    MULTI 

**Time complexity:** O(1)

**ACL categories:** @fast, @transaction

Marks the start of a [transaction][tt] block.
Subsequent commands will be queued for atomic execution using `EXEC`.

[tt]: https://redis.io/topics/transactions

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): always `OK`.
