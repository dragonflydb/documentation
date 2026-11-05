---
description: Learn how to use Redis XGROUP, the container command for creating and managing stream consumer groups and their consumers in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP

<PageTitle title="Redis XGROUP Command (Documentation) | Dragonfly" />

## Syntax

    XGROUP

**Time complexity:** Depends on subcommand.

**ACL categories:** @slow, @stream, @write

This is a container command for stream consumer group management commands.

Currently, the following subcommands are supported:

- [XGROUP CREATE](./xgroup-create.md)
- [XGROUP CREATECONSUMER](./xgroup-createconsumer.md)
- [XGROUP DELCONSUMER](./xgroup-delconsumer.md)
- [XGROUP DESTROY](./xgroup-destroy.md)
- [XGROUP SETID](./xgroup-setid.md)
- [XGROUP HELP](./xgroup-help.md)

`XGROUP` with fewer than two arguments, other than `XGROUP HELP`, returns `ERR wrong number of arguments for 'xgroup' command`.
An unknown subcommand returns `ERR syntax error`.
