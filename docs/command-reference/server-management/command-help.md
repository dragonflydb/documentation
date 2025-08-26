---
description:  Learn how to use Redis COMMAND HELP to display usage information for COMMAND subcommands.
---

import PageTitle from '@site/src/components/PageTitle';

# COMMAND HELP

<PageTitle title="Redis COMMAND HELP Command (Documentation) | Dragonfly" />

## Syntax

    COMMAND HELP 

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

Return usage information for the supported `COMMAND` subcommands in this Dragonfly server.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of human-readable help lines.

## Examples

```shell
dragonfly> COMMAND HELP
1) (no subcommand)
2)     Return details about all commands.
3) INFO command-name
4)     Return details about specified command.
5) COUNT
6)     Return the total number of commands in this server.
```

## Tips

- The help reflects only subcommands currently supported by Dragonfly.
- `COMMAND DOCS` is not implemented and returns an error: "COMMAND DOCS Not Implemented".
- See also: [`COMMAND`](./command.md), [`COMMAND INFO`](./command-info.md), [`COMMAND COUNT`](./command-count.md)


