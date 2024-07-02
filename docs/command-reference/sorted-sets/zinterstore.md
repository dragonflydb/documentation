---
description: Learn how to use the Redis ZINTERSTORE command to intersect multiple sorted sets and store the result, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZINTERSTORE

<PageTitle title="Redis ZINTERSTORE Explained (Better Than Official Docs)" />

## Syntax

    ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>]

**Time complexity:** O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.

**ACL categories:** @write, @sortedset, @slow

Computes the intersection of `numkeys` sorted sets given by the specified keys,
and stores the result in `destination`.
It is mandatory to provide the number of input keys (`numkeys`) before passing
the input keys and the other (optional) arguments.

By default, the resulting score of an element is the sum of its scores in the
sorted sets where it exists.
Because intersection requires an element to be a member of every given sorted
set, this results in the score of every element in the resulting sorted set to
be equal to the number of input sorted sets.

For a description of the `WEIGHTS` and `AGGREGATE` options, see `ZUNIONSTORE`.

If `destination` already exists, it is overwritten.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements in the resulting sorted set at
`destination`.

## Examples

```shell
dragonfly> ZADD zset1 1 "one"
(integer) 1
dragonfly> ZADD zset1 2 "two"
(integer) 1
dragonfly> ZADD zset2 1 "one"
(integer) 1
dragonfly> ZADD zset2 2 "two"
(integer) 1
dragonfly> ZADD zset2 3 "three"
(integer) 1
dragonfly> ZINTERSTORE out 2 zset1 zset2 WEIGHTS 2 3
(integer) 2
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "one"
2) "5"
3) "two"
4) "10"
```
