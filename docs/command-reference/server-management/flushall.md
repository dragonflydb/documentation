---
description:  Learn how to use Redis FLUSHALL command to delete all keys in every database.
---

import PageTitle from '@site/src/components/PageTitle';

# FLUSHALL

<PageTitle title="Redis FLUSHALL Command (Documentation) | Dragonfly" />

## Syntax

    FLUSHALL [ASYNC | SYNC]

**Time complexity:** O(N) where N is the total number of keys in all databases

**ACL categories:** @keyspace, @write, @slow, @dangerous

Delete all the keys of all the existing databases, not just the currently selected one.
This command never fails.

`FLUSHALL` will always asynchronously flush databases. Specifying `ASYNC` or `SYNC` does not currently affect the behavior.

Note: an asynchronous `FLUSHALL` command only deletes keys that were present at the time the command was invoked. Keys created during an asynchronous flush will be unaffected.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): OK
