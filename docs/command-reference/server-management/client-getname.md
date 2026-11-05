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

The `CLIENT GETNAME` returns the name of the current connection as set by `CLIENT SETNAME`. A new connection is named after its connection ID (the value that `CLIENT ID` returns) until a name is set. If the name was removed by setting it to an empty string, a null bulk reply is returned.

## Return

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): The connection name, or a null bulk reply if no name is set.
