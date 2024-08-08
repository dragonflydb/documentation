---
description: "Learn how to use Redis ACL DELUSER to remove specified users from the Access Control List and enhance datastore security."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL DELUSER

<PageTitle title="Redis ACL DELUSER Command (Documentation) | Dragonfly" />

## Syntax

    ACL DELUSER username [username ...]

**ACL categories:** @admin, @slow, @dangerous

Delete one or more ACL users and terminate all the connections that are authenticated with such users.
The `default` user cannot be removed from the system since it is the default user that every new connection is authenticated with.
The argument list may contain ACL users that do not exist.
In such cases, no operation is performed for the non-existent ACL users.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of users that were deleted.
This number will not always match the number of arguments since certain users may not exist.

## Examples

```shell
dragonfly> ACL SETUSER myuser ON >mypass +@string +@fast -@slow
OK

dragonfly> ACL DELUSER myuser
(integer) 1

dragonfly> ACL DELUSER non_existent_user
(integer) 0

dragonfly> ACL DELUSER default
(error) ERR The 'default' user cannot be removed
```
