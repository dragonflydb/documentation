---
description: Learn how to use the Redis ZINTER command to intersect multiple sorted sets
---

import PageTitle from '@site/src/components/PageTitle';

# ZINTER

<PageTitle title="Redis ZINTER Explained" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZINTER` command performs an **intersection** of multiple sorted sets.
It calculates the common members across the sets and returns the resulting set, where the score of each member in the result is computed based on the specified aggregation.

This command is particularly useful when you want to get the common elements of multiple user activity logs, product tags, or any system that relies on sorted sets, while also applying optional weights and custom aggregation to the scores.

## Syntax

```shell
ZINTER numkeys key [key ...]
  [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]
```

- **Time complexity:** O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `numkeys`: The number of sorted sets to be intersected.
- `key [key ...]`: The list of sorted sets to intersect.
- `WEIGHTS weight [weight ...]` (optional): Assigns weights to each sorted set for score multiplication.
- `AGGREGATE SUM | MIN | MAX` (optional): Determines how to aggregate the scores of members existing in multiple sets:
  - `SUM`: Adds the scores (this is the default behavior).
  - `MIN`: Takes the minimum score across the sets.
  - `MAX`: Takes the maximum score across the sets.
- `WITHSCORE` (optional): If specified, the command returns the score of each element along with the element itself.

## Return Values

- [Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays) the result of the intersection
- If `WITHSCORES` is provided, the array contains each element followed by its score.

## Code Examples

See [`ZINTERSTORE`](./zinterstore.md) command for more detailed explanation of optional parameters.

### Using `WITHSCORE` Option

```shell
dragonfly$> ZADD zset1 1 a 2 b
(integer) 2

dragonfly$> ZADD zset2 2 a 3 b
(integer) 2

127.0.0.1:6379> ZINTER 2 zset1 zset2 WITHSCORES
1) "a"
2) (double) 3  # Score: (1 + 2) = 2
3) "b"
4) (double) 5  # Score: (2 + 3) = 5
```



