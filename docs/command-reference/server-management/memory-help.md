---
description:  Learn how to use Redis MEMORY HELP command to know all the MEMORY subcommands.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY HELP

<PageTitle title="Redis MEMORY HELP Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY HELP 

**Time complexity:** O(1)

**ACL categories:** @slow

The `MEMORY HELP` command returns a helpful text describing the different
subcommands.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of subcommands and their descriptions
