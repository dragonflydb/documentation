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

Returns [Integer reply](https://redis.io/docs/reference/protocol-spec/#integers) of number of total commands in this Dragonfly server.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): number of commands returned by `COMMAND`

## Examples

```shell
dragonfly> COMMAND COUNT
(integer) 240
```
