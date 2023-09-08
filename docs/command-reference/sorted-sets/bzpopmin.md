---
description: BZPOPMIN is the blocking variant of the sorted set ZPOPMIN primitive
---

# BZPOPMIN

## Syntax

    BZPOPMIN key [key ...] timeout

**Time complexity:** O(log(N)) with N being the number of elements in the sorted set.

**ACL categories:** @write, @sortedset, @fast, @blocking

`BZPOPMIN` is the blocking variant of the sorted set [`ZPOPMIN`](./zpopmin.md) primitive.

It is the blocking version because it blocks the connection when there are no members to pop from any of the given sorted sets.
A member with the lowest score is popped from first sorted set that is non-empty, with the given keys being checked in the order that they are given.

The `timeout` argument is interpreted as a double value specifying the maximum number of seconds to block.
A timeout of zero can be used to block indefinitely.

See the [`BLPOP` documentation](../lists/blpop.md) for the exact semantics,
since `BZPOPMIN` is identical to [`BLPOP`](../lists/blpop.md)
with the only difference being the data structure being popped from.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays)), specifically:

- A `nil` multi-bulk when no element could be popped and the timeout expired.
- A three-element multi-bulk with the first element being the name of the key where a member was popped, the second element is the popped member itself, and the third element is the score of the popped element.

## Examples

```shell
dragonfly> DEL zset1 zset2
(integer) 0
dragonfly> ZADD zset1 0 a 1 b 2 c
(integer) 3
dragonfly> BZPOPMIN zset1 zset2 0
1) "zset1"
2) "a"
3) "0"
```
