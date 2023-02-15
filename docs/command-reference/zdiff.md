---
description: Subtract multiple sorted sets
---

# ZDIFF

## Syntax

    ZDIFF numkeys key [key ...] [WITHSCORES]

**Time complexity:** O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.

This command is similar to `ZDIFFSTORE`, but instead of storing the resulting
sorted set, it is returned to the client.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): the result of the difference (optionally with their scores, in case
the `WITHSCORES` option is given).

## Examples

```cli
ZADD zset1 1 "one"
ZADD zset1 2 "two"
ZADD zset1 3 "three"
ZADD zset2 1 "one"
ZADD zset2 2 "two"
ZDIFF 2 zset1 zset2
ZDIFF 2 zset1 zset2 WITHSCORES
```
