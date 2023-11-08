---
description:  Discover how to use Redis SLOWLOG HELP command to retrieve the current number of entries in the slow log.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG HELP

<PageTitle title="Redis SLOWLOG HELP Command (Documentation) | Dragonfly" />

## Syntax

    SLOWLOG HELP

The `SLOWLOG HELP` command returns a helpful text describing the different subcommands.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of subcommands and their descriptions.
