---
description: Remove one or more members from a sorted set
---

# ZREM

## Syntax

    ZREM key member [member ...]

**Time complexity:** O(M*log(N)) with N being the number of elements in the sorted set and M the number of elements to be removed.

Removes the specified members from the sorted set stored at `key`.
Non existing members are ignored.

An error is returned when `key` exists and does not hold a sorted set.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* The number of members removed from the sorted set, not including non existing
  members.

## Examples

```cli
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZADD myzset 3 "three"
ZREM myzset "two"
ZRANGE myzset 0 -1 WITHSCORES
```
