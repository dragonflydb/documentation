---
description: Return a range of members in a sorted set, by lexicographical
  range, ordered from higher to lower strings.
---

# ZREVRANGEBYLEX

## Syntax

    ZREVRANGEBYLEX key max min [LIMIT offset count]

**Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).

When all the elements in a sorted set are inserted with the same score, in order to force lexicographical ordering, this command returns all the elements in the sorted set at `key` with a value between `max` and `min`.

Apart from the reversed ordering, `ZREVRANGEBYLEX` is similar to `ZRANGEBYLEX`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of elements in the specified score range.

## Examples

```shell
dragonfly> ZADD myzset 0 a 0 b 0 c 0 d 0 e 0 f 0 g
(integer) 7
dragonfly> ZREVRANGEBYLEX myzset [c -
1) "c"
2) "b"
3) "a"
dragonfly> ZREVRANGEBYLEX myzset (c -
1) "b"
2) "a"
dragonfly> ZREVRANGEBYLEX myzset (g [aaa
1) "f"
2) "e"
3) "d"
4) "c"
5) "b"
```
