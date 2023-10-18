---
description:  Learn how to use Redis ZLEXCOUNT command to count elements in a sorted set between two given lexicographical values.
---

import PageTitle from '@site/src/components/PageTitle';

# ZLEXCOUNT

<PageTitle title="Redis ZLEXCOUNT Command (Documentation) | Dragonfly" />

## Syntax

    ZLEXCOUNT key min max

**Time complexity:** O(log(N)) with N being the number of elements in the sorted set.

**ACL categories:** @read, @sortedset, @fast

When all the elements in a sorted set are inserted with the same score, in order to force lexicographical ordering, this command returns the number of elements in the sorted set at `key` with a value between `min` and `max`.

The `min` and `max` arguments have the same meaning as described for
`ZRANGEBYLEX`.

Note: the command has a complexity of just O(log(N)) because it uses elements ranks (see `ZRANK`) to get an idea of the range. Because of this there is no need to do a work proportional to the size of the range.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements in the specified score range.

## Examples

```shell
dragonfly> ZADD myzset 0 a 0 b 0 c 0 d 0 e
(integer) 5
dragonfly> ZADD myzset 0 f 0 g
(integer) 2
dragonfly> ZLEXCOUNT myzset - +
(integer) 7
dragonfly> ZLEXCOUNT myzset [b [f
(integer) 5
```
