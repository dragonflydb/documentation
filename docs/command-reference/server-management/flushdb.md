---
description:  Learn how to use Redis FLUSHDB command to remove all keys from the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# FLUSHDB

<PageTitle title="Redis FLUSHDB Command (Documentation) | Dragonfly" />

## Syntax

    FLUSHDB

**Time complexity:** O(N) where N is the number of keys in the selected database

**ACL categories:** @keyspace, @write, @slow, @dangerous

Delete all the keys of the currently selected DB.
This command never fails.

Note: an asynchronous `FLUSHDB` command only deletes keys that were present at the time the command was invoked. Keys created during an asynchronous flush will be unaffected.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings)
