---
description: Learn how to use Redis XGROUP HELP to list the XGROUP subcommands that Dragonfly supports, and which ACL rules grant it.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP HELP

<PageTitle title="Redis XGROUP HELP Command (Documentation) | Dragonfly" />

## Syntax

    XGROUP HELP

**Time complexity:** O(1)

**ACL categories:** @read, @slow, @stream

The `XGROUP HELP` command returns a helpful text describing the different [`XGROUP`](./xgroup.md) subcommands supported by Dragonfly.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a list of subcommands and their descriptions.

## Examples

```shell
dragonfly> XGROUP HELP
 1) XGROUP <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
 2) CREATE <key> <groupname> <id|$> [option]
 3)     Create a new consumer group. Options are:
 4)     * MKSTREAM
 5)       Create the empty stream if it does not exist.
 6)     * ENTRIESREAD entries_read
 7)       Set the group's entries_read counter (internal use).
 8) CREATECONSUMER <key> <groupname> <consumer>
 9)     Create a new consumer in the specified group.
10) DELCONSUMER <key> <groupname> <consumer>
11)     Remove the specified consumer.
12) DESTROY <key> <groupname>
13)     Remove the specified group.
14) SETID <key> <groupname> <id|$> [ENTRIESREAD entries_read]
15)     Set the current group ID and entries_read counter.
16) HELP
17)     Print this help.
```

The help text lists `ENTRIESREAD` as an option of `XGROUP CREATE`, but Dragonfly accepts the option there and ignores it.
The `entries-read` counter of the new group stays unset, and [`XINFO GROUPS`](./xinfo-groups.md) reports it as nil.
In Valkey, the option sets the counter.
In Dragonfly, set the counter with [`XGROUP SETID`](./xgroup-setid.md) and `ENTRIESREAD entries_read`.
`XGROUP CREATE` reads `MKSTREAM` only directly after the ID and ignores every later argument, so `MKSTREAM` after `ENTRIESREAD` has no effect and the command fails if the stream does not exist.

## ACL Permissions

Dragonfly serves `XGROUP HELP` with the hidden command `_XGROUP_HELP` and checks ACL rules against it, not against `XGROUP`.
Its categories are `@read`, `@slow` and `@stream`, while `XGROUP` is in `@slow`, `@stream` and `@write`.
A `+xgroup` rule therefore does not grant `XGROUP HELP`, and `-xgroup` does not revoke it.
Grant it with `+_xgroup_help` or with one of its categories.
In Valkey, `+xgroup` grants `XGROUP HELP` together with the other subcommands.

Running `XGROUP HELP` without the permission returns `NOPERM <username> has no ACL permissions`.
`ACL DRYRUN` names the hidden command:

```shell
dragonfly> ACL SETUSER stream-admin ON >secret ~* -@all +xgroup
OK
dragonfly> ACL DRYRUN stream-admin XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> ACL DRYRUN stream-admin XGROUP HELP
"This user has no permissions to run the '_XGROUP_HELP' command"
dragonfly> ACL SETUSER stream-admin +_xgroup_help
OK
dragonfly> ACL DRYRUN stream-admin XGROUP HELP
OK
```
