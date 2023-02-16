---
description: Count the members in a sorted set with scores within the given values
---

# ZCOUNT

## Syntax

    ZCOUNT key min max

**Time complexity:** O(log(N)) with N being the number of elements in the sorted set.

Returns the number of elements in the sorted set at `key` with a score between
`min` and `max`.

The `min` and `max` arguments have the same semantic as described for
`ZRANGEBYSCORE`.

Note: the command has a complexity of just O(log(N)) because it uses elements ranks (see `ZRANK`) to get an idea of the range. Because of this there is no need to do a work proportional to the size of the range.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of elements in the specified score range.

## Examples

```cli
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZADD myzset 3 "three"
ZCOUNT myzset -inf +inf
ZCOUNT myzset (1 3
```
