---
description: "Learn to use Redis RANDOMKEY command to return random key from selected database."
---

import PageTitle from '@site/src/components/PageTitle';

# RANDOMKEY

<PageTitle title="Redis RANDOMKEY Command (Documentation) | Dragonfly" />

## Syntax

    RANDOMKEY

**Time complexity:** O(1).

**ACL categories:** @keyspace, @read, @slow

Return a random key from the currently selected database.

## Return

- [Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): A random key in database.
- `nil` when the database is empty.