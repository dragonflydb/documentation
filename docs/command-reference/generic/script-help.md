---
description: "Use Redis SCRIPT HELP command to understand script debugging capabilities."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT HELP

<PageTitle title="Redis SCRIPT HELP Command (Documentation) | Dragonfly" />

## Syntax

    SCRIPT HELP

**Time complexity:** O(1)

**ACL categories:** @slow, @scripting

The `SCRIPT HELP` command returns a helpful text describing the different subcommands.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of subcommands and their descriptions
