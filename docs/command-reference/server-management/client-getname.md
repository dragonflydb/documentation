---
description:  Learn how to use Redis CLIENT GETNAME command to fetch name of current connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT GETNAME

<PageTitle title="Redis CLIENT GETNAME Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT GETNAME

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

The `CLIENT GETNAME` returns the name of the current connection as set by `CLIENT SETNAME`. Since every new connection starts without an associated name, if no name was assigned a null bulk reply is returned.

## Return

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): The connection name, or a null bulk reply if no name is set.
