---
description: Learn how to use the Redis ZINTERSTORE command to intersect multiple sorted sets and store the result, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZINTERSTORE

<PageTitle title="Redis ZINTERSTORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZINTERSTORE` command performs an intersection of multiple sorted sets.
It calculates the common members across the sets and stores the result in a new sorted set, where the score of each member in the result is computed based on the specified aggregation.

This command is particularly useful when you want to get the common elements of multiple user activity logs, product tags, or any system that relies on sorted sets, while also applying optional weights and custom aggregation to the scores.

## Syntax

```shell
ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
```

- **Time complexity:** O(N*K)+O(M*log(M)) worst case with N being the smallest input sorted set, K being the number of input sorted sets and M being the number of elements in the resulting sorted set.
- **ACL categories:** @write, @sortedset, @slow

## Parameter Explanations

- `destination`: The key where the result of the operation will be stored.
- `numkeys`: The number of sorted sets to be intersected.
- `key [key ...]`: The list of sorted sets to intersect.
- `WEIGHTS weight [weight ...]` (optional): Assigns weights to each sorted set for score multiplication.
- `AGGREGATE SUM|MIN|MAX` (optional): Determines how to aggregate the scores of members existing in multiple sets:
  - `SUM`: Adds the scores (this is the default behavior).
  - `MIN`: Takes the minimum score across the sets.
  - `MAX`: Takes the maximum score across the sets.

## Return Values

The command returns the number of elements in the resulting sorted set, stored in `destination`.

## Code Examples

### Basic Example

Intersect two sorted sets and store the result in a new set:

```shell
dragonfly> ZADD zset1 1 a 2 b 3 c
(integer) 3
dragonfly> ZADD zset2 2 a 3 b 1 d
(integer) 3
dragonfly> ZINTERSTORE out 2 zset1 zset2
(integer) 2
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "a"
2) "3"  # Score is 1 + 2 = 3
3) "b"
4) "5"  # Score is 2 + 3 = 5
```

### Using `WEIGHTS` Option

Apply weights to each sorted set before calculating the intersection:

```shell
dragonfly> ZADD zset1 1 a 2 b
(integer) 2
dragonfly> ZADD zset2 2 a 3 b
(integer) 2
dragonfly> ZINTERSTORE out 2 zset1 zset2 WEIGHTS 2 3
(integer) 2
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "a"
2) "8"  # Score: (1 * 2) + (2 * 3) = 8
3) "b"
4) "13" # Score: (2 * 2) + (3 * 3) = 13
```

### Using `AGGREGATE` Option

Change the default aggregation method to `MIN` or `MAX`:

```shell
# Using MIN aggregation
dragonfly> ZADD zset1 1 a 5 b
(integer) 2
dragonfly> ZADD zset2 3 a 2 b
(integer) 2
dragonfly> ZINTERSTORE out 2 zset1 zset2 AGGREGATE MIN
(integer) 2
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "a"
2) "1"  # Minimum score of 'a'
3) "b"
4) "2"  # Minimum score of 'b'

# Using MAX aggregation
dragonfly> ZINTERSTORE out 2 zset1 zset2 AGGREGATE MAX
(integer) 2
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "a"
2) "3"  # Maximum score of 'a'
3) "b"
4) "5"  # Maximum score of 'b'
```

## Best Practices

- Use the `WEIGHTS` option to flexibly change how scores from each set contribute to the final result.
- Apply the `AGGREGATE` option to control how overlapping scores are combined — this can help tailor performance metrics, leaderboards, or analytics data.
- It's advisable to use the `ZINTERSTORE` command when intersecting relatively small sorted sets to minimize the risk of executing resource-heavy operations.

## Common Mistakes

- Using `SUM` aggregation without realizing it's the default; ensure it's the intended behavior before omitting the `AGGREGATE` parameter.
- Not accounting for the fact that `ZINTERSTORE` overwrites the destination key if it exists.
- Forgetting that weights are applied in order to the corresponding sorted sets, meaning you'll need to provide as many weights as there are sets.

## FAQs

### What happens if the destination key already exists?

`ZINTERSTORE` will overwrite the destination key with the new computed sorted set.

### Can I intersect sets with different numbers of members?

Yes, but only members common to all sets will be present in the result. The scores will be computed based on the specified weights and aggregation.

### What happens if a sorted set does not exist?

If a key for one of the specified sorted sets does not exist or is empty, it is treated as an empty set, leading to an empty result wherever that key is involved.
