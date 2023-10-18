---
description:  Learn how to use Redis DBSIZE command to fetch the number of keys in the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# DBSIZE

<PageTitle title="Redis DBSIZE Command (Documentation) | Dragonfly" />

## Syntax

    DBSIZE 

**Time complexity:** O(1)

**ACL categories:** @keyspace, @read, @fast

Return the number of keys in the currently-selected database.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers)
