---
description: Store a range of members from sorted set into another key
---

# ZRANGESTORE

## Syntax

    ZRANGESTORE dst src min max [BYSCORE | BYLEX] [REV] [LIMIT offset count]

**Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements stored into the destination key.

This command is like `ZRANGE`, but stores the result in the `<dst>` destination key.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of elements in the resulting sorted set.

## Examples

```cli
ZADD srczset 1 "one" 2 "two" 3 "three" 4 "four"
ZRANGESTORE dstzset srczset 2 -1
ZRANGE dstzset 0 -1
```
