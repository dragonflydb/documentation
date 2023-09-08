---
description: Remove all keys from all databases
---

# FLUSHALL

## Syntax

    FLUSHALL

**Time complexity:** O(N) where N is the total number of keys in all databases

**ACL categories:** @keyspace, @write, @slow, @dangerous

Delete all the keys of all the existing databases, not just the currently selected one.
This command never fails.

Note: an asynchronous `FLUSHALL` command only deletes keys that were present at the time the command was invoked. Keys created during an asynchronous flush will be unaffected.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings)
