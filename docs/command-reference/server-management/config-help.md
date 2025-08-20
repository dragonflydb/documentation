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

## Subcommands listed

The output includes the following entries as implemented in Dragonfly:

```
CONFIG <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
GET <pattern>
    Return parameters matching the glob-like <pattern> and their values.
SET <directive> <value>
    Set the configuration <directive> to <value>.
RESETSTAT
    Reset statistics reported by the INFO command.
REWRITE
    Rewrite the configuration file with the current configuration.
HELP
    Prints this help.
```
