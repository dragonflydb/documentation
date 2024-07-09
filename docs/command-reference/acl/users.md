---
description: Print the usernames of all users
---

import PageTitle from '@site/src/components/PageTitle';

# ACL USERS

<PageTitle title="Redis ACL USERS Command (Documentation) | Dragonfly" />

## Syntax

    ACL USERS

**ACL categories:** @admin, @slow, @dangerous

Shows a list of all the usernames in Dragonfly.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays)

## Examples

```shell
dragonfly> ACL USERS
1) john
2) mike
3) default
```
