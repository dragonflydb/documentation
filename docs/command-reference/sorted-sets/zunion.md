---
description: Learn how to use Redis ZUNION command to perform a union of multiple sorted sets, getting the sorted set of unique elements.
---

import PageTitle from '@site/src/components/PageTitle';

# ZUNION

<PageTitle title="Redis ZUNION Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZUNION` command is used to perform a union operation across multiple sorted sets (`zsets`) and return the resulting set.
The resulting set members are calculated by combining scores across input sorted sets.
It is particularly beneficial when you want to merge ranking or leaderboard data from multiple different sources or weight specific input sets differently.

## Syntax

```shell
ZUNION numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
```

- **Time complexity:** O(N)+O(M\*log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `numkeys`: The number of sorted sets to be unioned.
- `key`: The keys of the input sorted sets.
- `WEIGHTS` (optional): A list of weights that can be applied to each set's scores before performing the union.
- `AGGREGATE` (optional): Specifies how scores across sets are aggregated. The available options are:
  - `SUM` (default): The scores are summed.
  - `MIN`: The minimum score is taken.
  - `MAX`: The maximum score is taken.

## Return Values

The command returns the union of the sorted set members from the input `key`s, along with their aggregated scores based on the specified `AGGREGATE` method.

## Code Examples

### Basic Example: Union of Two Sorted Sets

Perform a union of two `zsets` and aggregate their scores by default (i.e., using `SUM`).

```shell
dragonfly> ZADD zset1 1 "apple" 2 "banana"
(integer) 2
dragonfly> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2
dragonfly> ZUNION 2 zset1 zset2
1) "apple"
2) (double) 4
3) "cherry"
4) (double) 4
5) "banana"
6) (double) 2
```

In this example, `"apple"` appears in both sorted sets, and its scores (`1` from `zset1` and `3` from `zset2`) are summed to give a final score of `4`.

### Using `WEIGHTS` Parameter

Assign different weights to the scores of different `zsets` before performing the union.

```shell
dragonfly> ZADD zset1 1 "apple" 2 "banana"
(integer) 2
dragonfly> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2
dragonfly> ZUNION 2 zset1 zset2 WEIGHTS 2 1
1) "apple"
2) (double) 5  # 1*2 + 3*1 = 5
3) "banana"
4) (double) 4  # 2*2 = 4
5) "cherry"
6) (double) 4  # 0 + 4*1 = 4
```

In this example, the score of `zset1` is multiplied by `2`, and the score of `zset2` is multiplied by `1`.

### Using the `AGGREGATE` Parameter: MIN Aggregation

Take the minimum score for members that exist in multiple sets, instead of summing them.

```shell
dragonfly> ZADD zset1 1 "apple" 6 "banana"
(integer) 2
dragonfly> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2
dragonfly> ZUNION 2 zset1 zset2 AGGREGATE MIN
1) "apple"
2) (double) 1  # min(1,3) = 1
3) "cherry"
4) (double) 4
5) "banana"
6) (double) 6
```

In this example, for `"apple"`, the lower score between the two sets was `1`, so it was selected.

### Weighting and Custom Aggregation: MAX Aggregation with Weights

Use both `WEIGHTS` and `AGGREGATE` to calculate the weighted `MAX` score for each member.

```shell
dragonfly> ZADD zset1 1 "apple" 6 "banana"
(integer) 2
dragonfly> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2
dragonfly> ZUNION 2 zset1 zset2 WEIGHTS 2 3 AGGREGATE MAX
1) "apple"
2) (double) 9  # max(1*2, 3*3) = 9
3) "cherry"
4) (double) 12  # 0 + 4*3 = 12
5) "banana"
6) (double) 12  # 6*2 = 12
```

In this example, weighted scores are calculated (`2x` for `zset1` and `3x` for `zset2`), and the maximum score is taken between sets.

## Best Practices

- Use `WEIGHTS` when input sorted sets contribute unequally to the final result, such as giving more significance to scores from more recent activity.
- Choose the appropriate `AGGREGATE` method based on your use case.
  For example, `MIN` is useful for retaining the smallest score across sets, and `MAX` is good for ranking systems where the highest rank should dominate.

## Common Mistakes

- Forgetting that `ZUNION` can return an empty set if none of the members from the input sets overlap.
- Assuming the result set will be sorted automatically by member names.
  The members are returned sorted by their aggregated scores.

## FAQs

### What happens if some of the keys do not exist?

If a key does not exist, it is treated as an empty sorted set and does not affect the result.
For example, if `zset1` doesn't exist in the above examples, only `zset2`'s members will be used to compute the result.

### Can I use other aggregation methods besides `SUM`, `MIN`, or `MAX`?

No, `SUM`, `MIN`, and `MAX` are the only supported aggregation methods.
If no method is specified, the default aggregation is `SUM`.

### What if the sets contain members with identical scores?

If the members have identical scores, they are included in the result.
However, there is no guaranteed order for members with the same score.
Another Redis command like `ZRANGE` can be used to further control the order.
