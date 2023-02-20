---
description: Add multiple sorted sets
---

# ZUNION

## Syntax

    ZUNION numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]

**Time complexity:** O(N)+O(M*log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.

This command is similar to `ZUNIONSTORE`, but instead of storing the resulting
sorted set, it is returned to the client.

For a description of the `WEIGHTS` and `AGGREGATE` options, see `ZUNIONSTORE`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): the result of union (optionally with their scores, in case 
the `WITHSCORES` option is given).

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
dragonfly> ZUNION 2 zset1 zset2
1) "one"
2) "three"
3) "two"
dragonfly> ZUNION 2 zset1 zset2 WITHSCORES
1) "one"
2) "2"
3) "three"
4) "3"
5) "two"
6) "4"
```
