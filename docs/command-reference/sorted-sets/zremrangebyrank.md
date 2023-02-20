---
description: Remove all members in a sorted set within the given indexes
---

# ZREMRANGEBYRANK

## Syntax

    ZREMRANGEBYRANK key start stop

**Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.

Removes all elements in the sorted set stored at `key` with rank between `start`
and `stop`.
Both `start` and `stop` are `0` -based indexes with `0` being the element with
the lowest score.
These indexes can be negative numbers, where they indicate offsets starting at
the element with the highest score.
For example: `-1` is the element with the highest score, `-2` the element with
the second highest score and so forth.

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
dragonfly> ZREMRANGEBYRANK myzset 0 1
(integer) 2
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "three"
2) "3"
```
