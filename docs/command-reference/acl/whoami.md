---
description: "Learn how to use Redis ACL WHOAMI to return the name of the authenticated user."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL WHOAMI

<PageTitle title="Redis ACL WHOAMI Command (Documentation) | Dragonfly" />

## Syntax

    ACL WHOAMI

**ACL categories:** @slow

Return the username the current connection is authenticated with.

## Return

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the username of the current connection.

## Examples

```shell
dragonfly> ACL WHOAMI
"default"
```
