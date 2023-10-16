---
description: Persist currently defined ACL's to file
---

# ACL SAVE

## Syntax

    ACL SAVE

**ACL categories:** @admin, @slow, @dangerous

When Dragonfly is configured to use an ACL file (with the `--aclfile` configuration option), this command will save the currently defined ACLs state to the ACL file.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` on success.
The error otherwise.

## Examples

```shell
dragonfly> ACL SAVE
"OK"
```
