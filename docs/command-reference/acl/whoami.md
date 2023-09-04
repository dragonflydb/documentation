---
description: Return which user is authenticated with the current connection
---

# ACL WHOAMI
**ACL categories:** @slow

## Syntax

    ACL WHOAMI

Return which user is authenticated with the current connection


## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `username` of the connected user


## Examples

```shell
dragonfly> ACL WHOAMI
"default"
```
