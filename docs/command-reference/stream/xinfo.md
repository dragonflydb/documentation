---
description: Learn how to use Redis XINFO, the container command for inspecting streams, their consumer groups, and consumers in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO

<PageTitle title="Redis XINFO Command (Documentation) | Dragonfly" />

## Syntax

    XINFO

**Time complexity:** Depends on subcommand.

**ACL categories:** @read, @slow, @stream

This is a container command for stream introspection commands.

Currently, the following subcommands are supported:

- [XINFO CONSUMERS](./xinfo-consumers.md)
- [XINFO GROUPS](./xinfo-groups.md)
- [XINFO STREAM](./xinfo-stream.md)
- [XINFO HELP](./xinfo-help.md)

Every subcommand, including `XINFO HELP`, is checked as `XINFO` itself, so `+xinfo` and `-xinfo` cover all of them and category rules use the categories of `XINFO`.

`XINFO` without arguments returns `ERR wrong number of arguments for 'xinfo' command`.
An unknown subcommand returns an error that names it, for example `ERR Unknown subcommand or wrong number of arguments for 'FOO'. Try XINFO HELP.`
