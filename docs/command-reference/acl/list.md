---
description: Returh which user is authenticated with the current connection
---

# ACL LIST

## Syntax

    ACL LIST

**ACL categories:** @admin, @slow, @dangerous

This command returns an array of the different users and their respective ACL rules.
Each line consists of the username, followed by a 15 char preview of the hashed password, their status (ON/OFF) and their rules.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): An array of strings. This command **does not explicitly report the removed ACL categories**.
For example, if a user was created in Redis with `-@fast`, `ACL LIST` would print `-@fast` for that given user.
We found that this redundancy is confusing to the user, and therefore we decided not to include it in the result string
because if for a given user a command category is missing, it's a clear indicator that this user does not have that rule in their ACL list.

## Examples

```shell
dragonfly> ACL LIST
1) "user george on #9f86d081884c7d +@admin +@fast"
2) "user default on nopass +@all"
```
