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

Delete all the keys for all the existing databases, not just the currently selected one.
This command never fails.

## Notes

- The `FLUSHALL` command always deletes keys asynchronously.
  It only deletes keys that were present at the time the command was invoked.
  Keys created during the deletion will be unaffected.
- However, if the `SYNC` option is specified, the command waits for the deletion (which is still asynchronous) to finish.
  Because of this, unlike Redis/Valkey, this command never blocks other commands.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK`.
