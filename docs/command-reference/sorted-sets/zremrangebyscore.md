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

```cli
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZADD myzset 3 "three"
ZREMRANGEBYSCORE myzset -inf (2
ZRANGE myzset 0 -1 WITHSCORES
```
