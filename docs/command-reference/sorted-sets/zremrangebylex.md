---
description: Use Redis ZREMRANGEBYLEX to remove sorted set members within a lexicographical range, plus expert tips beyond official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYLEX

<PageTitle title="Redis ZREMRANGEBYLEX Explained (Better Than Official Docs)" />

## Syntax

    ZREMRANGEBYLEX key min max

**Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.

**ACL categories:** @write, @sortedset, @slow

When all the elements in a sorted set are inserted with the same score, in order to force lexicographical ordering, this command removes all elements in the sorted set stored at `key` between the lexicographical range specified by `min` and `max`.

The meaning of `min` and `max` are the same of the `ZRANGEBYLEX` command. Similarly, this command actually removes the same elements that `ZRANGEBYLEX` would return if called with the same `min` and `max` arguments.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements removed.

## Examples

```shell
dragonfly> ZADD myzset 0 aaaa 0 b 0 c 0 d 0 e
(integer) 5
dragonfly> ZADD myzset 0 foo 0 zap 0 zip 0 ALPHA 0 alpha
(integer) 5
dragonfly> ZRANGE myzset 0 -1
1) "ALPHA"
2) "aaaa"
3) "alpha"
4) "b"
5) "c"
6) "d"
7) "e"
8) "foo"
9) "zap"
10) "zip"
dragonfly> ZREMRANGEBYLEX myzset [alpha [omega
(integer) 6
dragonfly> ZRANGE myzset 0 -1
1) "ALPHA"
2) "aaaa"
3) "zap"
4) "zip"
```
