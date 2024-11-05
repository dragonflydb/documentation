---
description: Learn how to use Redis ZUNIONSTORE command to apply set operations on sorted sets and store the resulting set in a new key.
---

import PageTitle from '@site/src/components/PageTitle';

# ZUNIONSTORE

<PageTitle title="Redis ZUNIONSTORE Explained (Better Than Official Docs)" />

## Syntax

    ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>]

**Time complexity:** O(N)+O(M log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.

**ACL categories:** @write, @sortedset, @slow

Computes the union of `numkeys` sorted sets given by the specified keys, and
stores the result in `destination`.
It is mandatory to provide the number of input keys (`numkeys`) before passing
the input keys and the other (optional) arguments.

By default, the resulting score of an element is the sum of its scores in the
sorted sets where it exists.

Using the `WEIGHTS` option, it is possible to specify a multiplication factor
for each input sorted set.
This means that the score of every element in every input sorted set is
multiplied by this factor before being passed to the aggregation function.
When `WEIGHTS` is not given, the multiplication factors default to `1`.

With the `AGGREGATE` option, it is possible to specify how the results of the
union are aggregated.
This option defaults to `SUM`, where the score of an element is summed across
the inputs where it exists.
When this option is set to either `MIN` or `MAX`, the resulting set will contain
the minimum or maximum score of an element across the inputs where it exists.

If `destination` already exists, it is overwritten.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements in the resulting sorted set at
`destination`.

## Examples

```shell
dragonfly$> ZADD zset1 1 "one"
(integer) 1
dragonfly$> ZADD zset1 2 "two"
(integer) 1
dragonfly$> ZADD zset2 1 "one"
(integer) 1
dragonfly$> ZADD zset2 2 "two"
(integer) 1
dragonfly$> ZADD zset2 3 "three"
(integer) 1
dragonfly$> ZUNIONSTORE out 2 zset1 zset2 WEIGHTS 2 3
(integer) 3
dragonfly$> ZRANGE out 0 -1 WITHSCORES
1) "one"
2) "5"
3) "three"
4) "9"
5) "two"
6) "10"
```
