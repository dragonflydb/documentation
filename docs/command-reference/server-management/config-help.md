---
description:  Learn how to use Redis CONFIG HELP command to list all CONFIG subcommands and their descriptions.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG HELP

<PageTitle title="Redis CONFIG HELP Command (Documentation) | Dragonfly" />

## Syntax

    CONFIG HELP

**Time complexity:** O(1)

**ACL categories:** @slow

The `CONFIG HELP` command returns a helpful text describing the different `CONFIG` subcommands supported by Dragonfly.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of subcommands and their descriptions.

## Example

The output of the `CONFIG HELP` command includes the following entries as implemented in Dragonfly:

```shell
dragonfly> CONFIG HELP
 1) CONFIG <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
 2) GET <pattern>
 3)     Return parameters matching the glob-like <pattern> and their values.
 4) SET <directive> <value>
 5)     Set the configuration <directive> to <value>.
 6) RESETSTAT
 7)     Reset statistics reported by the INFO command.
 8) REWRITE
 9)     Rewrite the configuration file with the current configuration.
10) HELP
11)     Prints this help.
```
