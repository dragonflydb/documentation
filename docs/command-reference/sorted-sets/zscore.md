---
description: Get the score associated with the given member in a sorted set
---

# ZSCORE

## Syntax

    ZSCORE key member

**Time complexity:** O(1)

**ACL categories:** @read, @sortedset, @fast

Returns the score of `member` in the sorted set at `key`.

If `member` does not exist in the sorted set, or `key` does not exist, `nil` is
returned.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the score of `member` (a double precision floating point number),
represented as string.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZSCORE myzset "one"
"1"
```
