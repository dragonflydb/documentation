---
description: Remove all members in a sorted set within the given scores
---

# ZREMRANGEBYSCORE

## Syntax

    ZREMRANGEBYSCORE key min max

**Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.

Removes all elements in the sorted set stored at `key` with a score between
`min` and `max` (inclusive).

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of elements removed.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREMRANGEBYSCORE myzset -inf (2
(integer) 1
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "two"
2) "2"
3) "three"
4) "3"
```
