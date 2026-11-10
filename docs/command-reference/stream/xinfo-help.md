---
description: Learn how to use Redis XINFO HELP to list the XINFO subcommands that Dragonfly supports for inspecting streams and consumer groups.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO HELP

<PageTitle title="Redis XINFO HELP Command (Documentation) | Dragonfly" />

## Syntax

    XINFO HELP

**Time complexity:** O(1)

**ACL categories:** @read, @slow, @stream

The `XINFO HELP` command returns a helpful text describing the different [`XINFO`](./xinfo.md) subcommands supported by Dragonfly.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a list of subcommands and their descriptions.
Unlike Valkey, the reply does not start with an `XINFO <subcommand> ...` summary line.

## Examples

```shell
dragonfly> XINFO HELP
1) CONSUMERS <key> <groupname>
2)     Show consumers of <groupname>.
3) GROUPS <key>
4)     Show the stream consumer groups.
5) STREAM <key> [FULL [COUNT <count>]
6)     Show information about the stream.
7) HELP
8)     Prints this help.
```
