---
description: Persist currently defined ACL's to file
---

# ACL SAVE

## Syntax

    ACL SAVE

**ACL categories:** @admin, @slow, @dangerous

When Dragonfly is configured to use an ACL file (with the `--aclfile` configuration option), this command will save the currently defined ACLs state to the ACL file.

Note, that Dragonfly should have write permissions for that file. For example, placing it in `/etc/` will not work because the directory is only
accessible as readonly by Dragonfly (see `/lib/systemd/system/dragonfly.service`). We advice to place acl files in `/var/lib/dragonfly/` unless
you plan them to be read only (and in that case it would make sense to store them in `/etc`).

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` on success.
The error otherwise.

## Examples

```shell
dragonfly> ACL SAVE
"OK"
```
