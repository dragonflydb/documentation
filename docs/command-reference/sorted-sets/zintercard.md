---
description: Learn how to use the Redis ZINTERCARD command to return intersection cardinality of multiple sorted sets
---

import PageTitle from '@site/src/components/PageTitle';

# ZINTERCARD

<PageTitle title="Redis ZINTERCARD Explained" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZINTERCARD` command performs an **intersection** of multiple sorted sets.
This command is similar to [`ZINTER`](./zinter.md), but instead of returning the result set, it returns just the cardinality of the result.

By default, the command calculates the cardinality of the intersection of all given sets. When provided with the optional `LIMIT` argument (which defaults to 0 and means unlimited), if the intersection cardinality reaches limit partway through the computation, the algorithm will exit and yield limit as the cardinality. 

## Syntax

```shell
ZINTERCARD numkeys key [key ...] [LIMIT limit]
```

- **Time complexity:** O(N*K) worst case with N being the smallest input sorted set, K being the number of input sorted sets.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `numkeys`: The number of sorted sets to be intersected.
- `key [key ...]`: The list of sorted sets to intersect.
- `LIMIT limit` (optional): Set cardinality limit

## Return Values

- [Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers) the cardinality (number of elements) of members in the resulting intersection.

## Code Examples

```shell
127.0.0.1:6379> ZADD zset1 1 a 2 b 3 c
(integer) 3

127.0.0.1:6379> ZADD zset2 1 a 2 b 3 c 4 d
(integer) 4

127.0.0.1:6379> ZINTER 2 zset1 zset2
1) "one"
2) "two"

127.0.0.1:6379> ZINTERCARD 2 zset1 zset2
(integer) 2

127.0.0.1:6379> ZINTERCARD 2 zset1 zset2 LIMIT 1
(integer) 1
```