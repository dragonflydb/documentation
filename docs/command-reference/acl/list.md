---
description: "Learn how to use Redis ACL LIST to retrieve the list of rules for all the existing users."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL LIST

<PageTitle title="Redis ACL LIST Command (Documentation) | Dragonfly" />

## Syntax

    ACL LIST

**ACL categories:** @admin, @slow, @dangerous

This command returns an array of the different users and their respective ACL rules.
Each line consists of the username, followed by their status (ON/OFF), a 15-character preview of the hashed password or `nopass`, and their rules.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): An array of strings. 

## Examples

```shell
dragonfly> ACL LIST
1) "user george on #9f86d081884c7d +@admin +@fast"
2) "user default on nopass +@all"
```
