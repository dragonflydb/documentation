---
description: Get total number of Dragonfly commands
---

# COMMAND COUNT

## Syntax

    COMMAND COUNT 

**Time complexity:** O(1)

**ACL categories:** @slow, @connection

Returns [Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers) of number of total commands in this Dragonfly server.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): number of commands returned by `COMMAND`

## Examples

```shell
dragonfly> COMMAND COUNT
(integer) 240
```
