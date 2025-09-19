---
description:  Learn how to use Redis FLUSHDB command to remove all keys from the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# FLUSHDB

<PageTitle title="Redis FLUSHDB Command (Documentation) | Dragonfly" />

## Syntax

    FLUSHDB [ASYNC | SYNC]

**Time complexity:** O(N) where N is the number of keys in the selected database

**ACL categories:** @keyspace, @write, @slow, @dangerous

Delete all the keys of the currently selected database.
This command never fails.

## Notes

- The `FLUSHDB` command always deletes keys asynchronously.
  It only deletes keys that were present at the time the command was invoked.
  Keys created during the deletion will be unaffected.
- However, if the `SYNC` option is specified, the command waits for the deletion (which is still asynchronous) to finish.
  Because of this, unlike Redis/Valkey, this command never blocks other commands.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK`.
