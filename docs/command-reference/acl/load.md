---
description: Load all ACL configuration from a file
---

# ACL LOAD

## Syntax

    ACL LOAD

**ACL categories:** @admin, @slow, @dangerous

When Dragonfly is configured to use an ACL file (with the `--aclfile` configuration option), this command will load the ACL rules into Dragonfly.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` on success.
The error otherwise.

## Examples

```shell
dragonfly> ACL LOAD
"OK"
```
