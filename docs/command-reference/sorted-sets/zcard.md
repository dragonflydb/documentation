---
description: Get the number of members in a sorted set
---

# ZCARD

## Syntax

    ZCARD key

**Time complexity:** O(1)

Returns the sorted set cardinality (number of elements) of the sorted set stored
at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the cardinality (number of elements) of the sorted set, or `0`
if `key` does not exist.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZCARD myzset
(integer) 2
```
