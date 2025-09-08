---
description: "Learn usage of Redis MOVE command that moves a key to another database."
---

import PageTitle from '@site/src/components/PageTitle';

# MOVE

<PageTitle title="Redis MOVE Command (Documentation) | Dragonfly" />

## Syntax

    MOVE key db

**Time complexity:** O(1)

**ACL categories:** @keyspace, @write, @fast

Move `key` from the currently selected database (see `SELECT`) to the specified
destination database.
When `key` already exists in the destination database, or it does not exist in
the source database, it does nothing.
It is possible to use `MOVE` as a locking primitive because of this.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers), specifically:

- `1` if `key` was moved.
- `0` if `key` was not moved.
