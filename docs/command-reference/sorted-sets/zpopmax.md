---
description: Remove and return members with the highest scores in a sorted set
---

# ZPOPMAX

## Syntax

    ZPOPMAX key [count]

**Time complexity:** O(log(N)*M) with N being the number of elements in the sorted set, and M being the number of elements popped.

Removes and returns up to `count` members with the highest scores in the sorted
set stored at `key`.

When left unspecified, the default value for `count` is 1. Specifying a `count`
value that is higher than the sorted set's cardinality will not produce an
error. When returning multiple elements, the one with the highest score will
be the first, followed by the elements with lower scores.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of popped elements and scores.

## Examples

```cli
ZADD myzset 1 "one"
ZADD myzset 2 "two"
ZADD myzset 3 "three"
ZPOPMAX myzset
```
