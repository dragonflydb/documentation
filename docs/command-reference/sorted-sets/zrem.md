---
description: Learn how to use the Redis ZREM command to remove members from a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREM

<PageTitle title="Redis ZREM Explained (Better Than Official Docs)" />

## Syntax

    ZREM key member [member ...]

**Time complexity:** O(M\*log(N)) with N being the number of elements in the sorted set and M the number of elements to be removed.

**ACL categories:** @write, @sortedset, @fast

Removes the specified members from the sorted set stored at `key`.
Non existing members are ignored.

An error is returned when `key` exists and does not hold a sorted set.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

- The number of members removed from the sorted set, not including non existing
  members.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREM myzset "two"
(integer) 1
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "one"
2) "1"
3) "three"
4) "3"
```
