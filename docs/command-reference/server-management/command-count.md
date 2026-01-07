---
description:  Learn how to use Redis COMMAND COUNT to count the total number of commands.
---

import PageTitle from '@site/src/components/PageTitle';

# COMMAND COUNT

<PageTitle title="Redis COMMAND COUNT Command (Documentation) | Dragonfly" />

## Syntax

    COMMAND COUNT

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

Returns the number of total commands in this Dragonfly server.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): number of commands returned by `COMMAND`.

## Examples

```shell
dragonfly> COMMAND COUNT
(integer) 283
```

## Tips

- Counts only non-hidden commands (commands marked with the `HIDDEN` flag are excluded from `COMMAND`).
- Equivalent to the number of elements returned by `COMMAND` without subcommands.

## See also

[`COMMAND`](./command.md) | [`COMMAND INFO`](./command-info.md)
