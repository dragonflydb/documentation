---
description: "Learn how to use Redis ACL HELP to list the ACL subcommands that Dragonfly supports, with a short description of each."
---

import PageTitle from '@site/src/components/PageTitle';

# ACL HELP

<PageTitle title="Redis ACL HELP Command (Documentation) | Dragonfly" />

## Syntax

    ACL HELP

**Time complexity:** O(1)

**ACL categories:** @slow

The `ACL HELP` command returns a helpful text describing the different [`ACL`](./acl.md) subcommands supported by Dragonfly.

`ACL HELP` has its own ACL entry, so a `+acl` rule does not grant it.
Grant it with `+acl|help` or with `+@slow`, as described in [Subcommand Permissions](./acl.md#subcommand-permissions).

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a list of subcommands and their descriptions.

## Examples

```shell
dragonfly> ACL HELP
 1) ACL <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
 2) CAT [<category>]
 3)     List all commands that belong to <category>, or all command categories
 4)     when no category is specified.
 5) DELUSER <username> [<username> ...]
 6)     Delete a list of users.
 7) DRYRUN <username> <command> [<arg> ...]
 8)     Returns whether the user can execute the given command without executing the command.
 9) GETUSER <username>
10)     Get the user's details.
11) GENPASS [<bits>]
12)     Generate a secure 256-bit user password. The optional `bits` argument can
13)     be used to specify a different size.
14) LIST
15)     Show users details in config file format.
16) LOAD
17)     Reload users from the ACL file.
18) LOG [<count> | RESET]
19)     Show the ACL log entries.
20) SAVE
21)     Save the current config to the ACL file.
22) SETUSER <username> <attribute> [<attribute> ...]
23)     Create or modify a user with the specified attributes.
24) USERS
25)     List all the registered usernames.
26) WHOAMI
27)     Return the current connection username.
28) HELP
29)     Print this help.
```
