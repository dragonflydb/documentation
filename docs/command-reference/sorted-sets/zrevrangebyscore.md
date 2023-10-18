---
description:  Learn how to use Redis ZREVRANGEBYSCORE command to retrieve members of a sorted set by score in descending order.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGEBYSCORE

<PageTitle title="Redis ZREVRANGEBYSCORE Command (Documentation) | Dragonfly" />

## Syntax

    ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]

**Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).

**ACL categories:** @read, @sortedset, @slow

Returns all the elements in the sorted set at `key` with a score between `max`
and `min` (including elements with score equal to `max` or `min`).
In contrary to the default ordering of sorted sets, for this command the
elements are considered to be ordered from high to low scores.

The elements having the same score are returned in reverse lexicographical
order.

Apart from the reversed ordering, `ZREVRANGEBYSCORE` is similar to
`ZRANGEBYSCORE`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): list of elements in the specified score range (optionally
with their scores).

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREVRANGEBYSCORE myzset +inf -inf
1) "three"
2) "two"
3) "one"
dragonfly> ZREVRANGEBYSCORE myzset 2 1
1) "two"
2) "one"
dragonfly> ZREVRANGEBYSCORE myzset 2 (1
1) "two"
dragonfly> ZREVRANGEBYSCORE myzset (2 (1
(empty array)
```
