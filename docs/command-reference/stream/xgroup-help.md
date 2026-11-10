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

