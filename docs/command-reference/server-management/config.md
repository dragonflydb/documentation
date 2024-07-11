---
description:  Learn how to use Redis CONFIG command to configure Redis server at runtime.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG

<PageTitle title="Redis CONFIG Command (Documentation) | Dragonfly" />

## Syntax

    CONFIG 

**Time complexity:** Depends on subcommand.

**ACL categories:** @slow

This is a container command for runtime configuration commands.
Currently, the following subcommands are supported:

- [`CONFIG GET`](./config-get.md)
- [`CONFIG RESETSTAT`](./config-resetstat.md)
- [`CONFIG SET`](./config-set.md)

<!-- To see the list of available commands you can call `CONFIG HELP`. -->
