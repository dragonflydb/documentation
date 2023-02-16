---
description: Watch the given keys to determine execution of the MULTI/EXEC block
---

# WATCH

## Syntax

    WATCH key [key ...]

**Time complexity:** O(1) for every key.

Marks the given keys to be watched for conditional execution of a
[transaction][tt].

[tt]: https://redis.io/topics/transactions

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): always `OK`.
