---
description: Remove and return the member with the lowest score from one or more
  sorted sets, or block until one is available
---

# BZPOPMIN

## Syntax

    BZPOPMIN key [key ...] timeout

**Time complexity:** O(log(N)) with N being the number of elements in the sorted set.

`BZPOPMIN` is the blocking variant of the sorted set `ZPOPMIN` primitive.

It is the blocking version because it blocks the connection when there are no
members to pop from any of the given sorted sets.
A member with the lowest score is popped from first sorted set that is
non-empty, with the given keys being checked in the order that they are given.

The `timeout` argument is interpreted as a double value specifying the maximum
number of seconds to block. A timeout of zero can be used to block indefinitely.

See the [BLPOP documentation][cl] for the exact semantics, since `BZPOPMIN` is
identical to `BLPOP` with the only difference being the data structure being
popped from.

[cl]: ./blpop.md

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): specifically:

* A `nil` multi-bulk when no element could be popped and the timeout expired.
* A three-element multi-bulk with the first element being the name of the key
  where a member was popped, the second element is the popped member itself,
  and the third element is the score of the popped element.

## Examples

```
redis> DEL zset1 zset2
(integer) 0
redis> ZADD zset1 0 a 1 b 2 c
(integer) 3
redis> BZPOPMIN zset1 zset2 0
1) "zset1"
2) "a"
3) "0"
```
