---
description: Return a random key from the keyspace
---

# RANDOMKEY

## Syntax

    RANDOMKEY 

**Time complexity:** O(1)

Return a random key from the currently selected database.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the random key, or `nil` when the database is empty.
