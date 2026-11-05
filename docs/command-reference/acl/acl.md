---
description: "Learn how to use Redis ACL, the container command for managing Dragonfly ACL users, permissions, and the ACL security log."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL

<PageTitle title="Redis ACL Command (Documentation) | Dragonfly" />

## Syntax

    ACL

**Time complexity:** Depends on subcommand.

**ACL categories:** @slow

This is a container command for Access Control List (ACL) commands.

Currently, the following subcommands are supported:

- [ACL CAT](./cat.md)
- [ACL DELUSER](./deluser.md)
- [ACL DRYRUN](./dryrun.md)
- [ACL GETUSER](./getuser.md)
- [ACL GENPASS](./genpass.md)
- [ACL LIST](./list.md)
- [ACL LOAD](./load.md)
- [ACL LOG](./log.md)
- [ACL SAVE](./save.md)
- [ACL SETUSER](./setuser.md)
- [ACL USERS](./users.md)
- [ACL WHOAMI](./whoami.md)
- [ACL HELP](./help.md)

`ACL` without a subcommand returns `ERR Wrong number of arguments for acl command`.
An unknown subcommand returns `` ERR unknown command `ACL` ``.

## Subcommand Permissions

Each `ACL` subcommand is a separate command with its own ACL categories, which are listed on its page.
The rules `+acl` and `-acl` apply only to the bare `ACL` command, so they neither grant nor revoke any subcommand.
This differs from Valkey, where `+acl` grants every `ACL` subcommand and `-acl` revokes them all.

To grant or revoke a single subcommand, use `+acl|<subcommand>` or `-acl|<subcommand>`, for example `+acl|whoami`.
Category rules work as usual.
`ACL CAT`, `ACL GENPASS`, `ACL WHOAMI` and `ACL HELP` are only in `@slow`.
The other subcommands are also in `@admin` and `@dangerous`, so `-@admin` revokes them.

In the following example, `-acl` does not stop the user from creating users, while `-acl|setuser` does:

```shell
dragonfly> ACL SETUSER app ON >secret +@all -acl
OK
dragonfly> ACL DRYRUN app ACL SETUSER alice ON
OK
dragonfly> ACL SETUSER app -acl|setuser
OK
dragonfly> ACL DRYRUN app ACL SETUSER alice ON
"This user has no permissions to run the 'ACL SETUSER' command"
```
