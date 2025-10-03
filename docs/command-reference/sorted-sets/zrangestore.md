---
description: Learn how to use the Redis ZRANGESTORE command to fetch elements in a specific range from a sorted set and store the result.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGESTORE

<PageTitle title="Redis ZRANGESTORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANGESTORE` command fetch elements in a specific range from a sorted set and store the result.

## Syntax

```shell
ZRANGESTORE destination key min max [BYSCORE | BYLEX] [REV] [LIMIT offset count]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements stored into the destination key.
- **ACL categories:** @write, @sortedset, @slow

This command is like [`ZRANGE`](./zrange.md), but stores the result in the `destination` key.

## Return Values

- [Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers) the number of elements in the resulting sorted set, stored in `destination`.

## Code Examples

```shell
dragonfly> ZADD key 1 one 2 two 3 three 4 four
(integer) 4
dragonfly> ZRANGESTORE dst key 1 3
(integer) 3
dragonfly> ZRANGE dst 0 -1
1) "two"
2) "three"
3) "four"
```
