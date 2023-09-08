---
description: Return which user is authenticated with the current connection
---

# ACL WHOAMI

## Syntax

    ACL WHOAMI

**ACL categories:** @slow

Return the username the current connection is authenticated with.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): the username of the current connection.

## Examples

```shell
dragonfly> ACL WHOAMI
"default"
```
