---
description: Learn to use the Redis ZMSCORE command to return scores for given members in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZMSCORE

<PageTitle title="Redis ZMSCORE Explained (Better Than Official Docs)" />

## Syntax

    ZMSCORE key member [member ...]

**Time complexity:** O(N) where N is the number of members being requested.

**ACL categories:** @read, @sortedset, @fast

Returns the scores associated with the specified `members` in the sorted set stored at `key`.

For every `member` that does not exist in the sorted set, a `nil` value is returned.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): list of scores or `nil` associated with the specified `member` values (a double precision floating point number),
represented as strings.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZMSCORE myzset "one" "two" "nofield"
1) "1"
2) "2"
3) (nil)
```
