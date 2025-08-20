---
description: Learn how to use Redis XINFO HELP command offering help with the numerous XINFO subcommands.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO HELP

<PageTitle title="Redis XINFO HELP Command (Documentation) | Dragonfly" />

## Syntax

    XINFO HELP

**Time complexity:** O(1)

The `XINFO HELP` command returns a helpful text describing the different subcommands.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of subcommands and their descriptions
