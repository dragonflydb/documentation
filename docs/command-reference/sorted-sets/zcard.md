---
description:  Learn to use Redis ZCARD command to get the total number of elements in a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZCARD

<PageTitle title="Redis ZCARD Command (Documentation) | Dragonfly" />

## Syntax

    ZCARD key

**Time complexity:** O(1)

**ACL categories:** @read, @sortedset, @fast

Returns the sorted set cardinality (number of elements) of the sorted set stored
at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the cardinality (number of elements) of the sorted set, or `0`
if `key` does not exist.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZCARD myzset
(integer) 2
```
