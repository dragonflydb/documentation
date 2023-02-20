---
description: Remove and return members with the lowest scores in a sorted set
---

# ZPOPMIN

## Syntax

    ZPOPMIN key [count]

**Time complexity:** O(log(N)*M) with N being the number of elements in the sorted set, and M being the number of elements popped.

Removes and returns up to `count` members with the lowest scores in the sorted
set stored at `key`.

When left unspecified, the default value for `count` is 1. Specifying a `count`
value that is higher than the sorted set's cardinality will not produce an
error. When returning multiple elements, the one with the lowest score will
be the first, followed by the elements with greater scores.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of popped elements and scores.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZPOPMIN myzset
1) "one"
2) "1"
```
