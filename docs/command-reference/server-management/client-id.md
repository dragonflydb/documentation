---
description:  Learn how to use Redis CLIENT ID to get the current connection's unique ID.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT ID

<PageTitle title="Redis CLIENT ID Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT ID

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

Return the unique ID of the current client connection.

The ID can be used with other client-management commands such as `CLIENT KILL ID <id>` or `CLIENT LIST` output correlation.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the current connection's client ID.

## Examples

```shell
dragonfly> CLIENT ID
(integer) 123
```


