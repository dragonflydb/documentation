---
description: Learn how to use Redis XGROUP HELP to obtain assistance while managing Redis Stream consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP HELP

<PageTitle title="Redis XGROUP HELP Explained (Better Than Official Docs)" />

## Syntax

    XGROUP HELP

**Time complexity:** O(1)

The `XGROUP HELP` command returns a helpful text describing the different subcommands.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of subcommands and their descriptions
