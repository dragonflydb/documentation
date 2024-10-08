---
description: Print ACL's of a user
---

import PageTitle from '@site/src/components/PageTitle';

# ACL GETUSER

<PageTitle title="Redis ACL GETUSER Command (Documentation) | Dragonfly" />

## Syntax

    ACL GETUSER username

**ACL categories:** @admin, @slow, @dangerous

The command returns all the rules defined for an existing ACL user.

## Return

- [Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of ACL rule definitions for the user.
- [Null reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): if the user does not exist.

## Examples

```shell
dragonfly> ACL GETUSER default
1) flags
2) 1) on
   2) nopass
3) passwords
4) (empty array)
5) commands
6) +@all
7) keys
8) ~*
9) channels
10) &*

dragonfly> ACL GETUSER non_existent_user
(nil)
```
