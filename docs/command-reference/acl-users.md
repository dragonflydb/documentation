---
description: List the username of all the configured ACL rules
---

# ACL USERS

## Syntax

    ACL USERS 

**Time complexity:** O(N). Where N is the number of configured users.

The command shows a list of all the usernames of the currently configured
users in the Redis ACL system.

## Return

An array of strings.

## Examples

```
> ACL USERS
1) "anna"
2) "antirez"
3) "default"
```
