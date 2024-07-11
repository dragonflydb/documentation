---
description: Learn to use the Redis ZINCRBY command to increment the score of a member in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZINCRBY

<PageTitle title="Redis ZINCRBY Explained (Better Than Official Docs)" />

## Syntax

    ZINCRBY key increment member

**Time complexity:** O(log(N)) where N is the number of elements in the sorted set.

**ACL categories:** @write, @sortedset, @fast

Increments the score of `member` in the sorted set stored at `key` by
`increment`.
If `member` does not exist in the sorted set, it is added with `increment` as
its score (as if its previous score was `0.0`).
If `key` does not exist, a new sorted set with the specified `member` as its
sole member is created.

An error is returned when `key` exists but does not hold a sorted set.

The `score` value should be the string representation of a numeric value, and
accepts double precision floating point numbers.
It is possible to provide a negative value to decrement the score.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): the new score of `member` (a double precision floating point
number), represented as string.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZINCRBY myzset 2 "one"
"3"
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "two"
2) "2"
3) "one"
4) "3"
```
