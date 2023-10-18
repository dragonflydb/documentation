---
description:  Learn to use Redis ZDIFF command to compute the difference between two or more sorted sets.
---

import PageTitle from '@site/src/components/PageTitle';

# ZDIFF

<PageTitle title="Redis ZDIFF Command (Documentation) | Dragonfly" />

## Syntax

    ZDIFF numkeys key [key ...] [WITHSCORES]

**Time complexity:** : O(L + K log K) worst case where L is the total number of elements in all the sets, and K is the size of the result set.

**ACL categories:** @read, @sortedset, @slow

This command is similar to ZDIFFSTORE, but instead of storing the resulting sorted set, it is returned to the client

## Return
[Array reply](https://redis.io/docs/reference/protocol-spec/#resp-arrays): the result of the difference (optionally with their scores, in case the WITHSCORES option is given).

## Examples

```shell
dragonfly> ZADD zset1 1 "one"
(integer) 1
dragonfly> ZADD zset1 2 "two"
(integer) 1
dragonfly> ZADD zset1 3 "three"
(integer) 1
dragonfly> ZADD zset2 1 "one"
(integer) 1
dragonfly> ZADD zset2 2 "two"
(integer) 1
dragonfly> ZDIFF 2 zset1 zset2
1) "three"
```
