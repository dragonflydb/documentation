---
description: Remove all keys from the current database
---

# FLUSHDB

## Syntax

    FLUSHDB

**Time complexity:** O(N) where N is the number of keys in the selected database

Delete all the keys of the currently selected DB.
This command never fails.

Note: an asynchronous `FLUSHDB` command only deletes keys that were present at the time the command was invoked. Keys created during an asynchronous flush will be unaffected.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)
