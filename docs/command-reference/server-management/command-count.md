---
description: Get total number of Redis commands
---

# COMMAND COUNT

## Syntax

    COMMAND COUNT 

**Time complexity:** O(1)

Returns [Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers) of number of total commands in this Redis server.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): number of commands returned by `COMMAND`

## Examples

```shell
dragonfly> COMMAND COUNT
(integer) 240
```
