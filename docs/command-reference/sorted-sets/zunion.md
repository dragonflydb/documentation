---
description: Learn how to use Redis ZUNION command to perform a union of multiple sorted sets, getting the sorted set of unique elements.
---

import PageTitle from '@site/src/components/PageTitle';

# ZUNION

<PageTitle title="Redis ZUNION Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZUNION` command is used to perform a union operation across multiple sorted sets (`zsets`) and return the resulting set.
The resulting set members are calculated by combining scores across input sorted sets.
This command can be used when you want to merge ranking or leaderboard data from multiple different sources or weight specific input sets differently.

## Syntax

```shell
ZUNION numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE <SUM | MIN | MAX>] [WITHSCORES]
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
- `WITHSCORES` (optional): If specified, the command returns the scores along with the members.

## Return Values

- The command returns the result of the union with, optionally, their scores when `WITHSCORES` is used.

## Code Examples

### Basic Example: Union of Two Sorted Sets

Perform a union of two sorted sets and aggregate their scores using the default `SUM` method.

```shell
dragonfly$> ZADD zset1 1 "apple" 2 "banana"
(integer) 2

dragonfly$> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2

dragonfly$> ZUNION 2 zset1 zset2 WITHSCORES
1) "banana"
2) "2"
3) "apple"
4) "4"
5) "cherry"
6) "4"
```

In this example, `apple` appears in both sorted sets, and its scores are summed to give a result of `4`.

### Using `WEIGHTS` Parameter

Assign different weights to the scores of different `zsets` before performing the union.

```shell
dragonfly$> ZADD zset1 1 "apple" 2 "banana"
(integer) 2

dragonfly$> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2

dragonfly$> ZUNION 2 zset1 zset2 WEIGHTS 2 1 WITHSCORES
1) "banana"
2) "4"        # 2x2 + 0x1 = 4
3) "cherry"
4) "4"        # 0x2 + 4x1 = 4
5) "apple"
6) "5"        # 1x2 + 3x1 = 5
```

In this example, scores of `zset1` are multiplied by `2`, and scores of `zset2` are multiplied by `1`.

### Using the `AGGREGATE` Parameter

Take the maximum or minimum score for members that exist in multiple sets, instead of summing them.

```shell
dragonfly$> ZADD zset1 1 "apple"
(integer) 1

dragonfly$> ZADD zset2 100 "apple"
(integer) 1

dragonfly$> ZUNION 2 zset1 zset2 AGGREGATE MIN WITHSCORES
1) "apple"
2) "1"

dragonfly$> ZUNION 2 zset1 zset2 AGGREGATE MAX WITHSCORES
1) "apple"
2) "100"
```

In this example, for `"apple"`, the lower score between the two sets was `1`, so it was selected.

### Using Both `WEIGHTS` and `AGGREGATE`

Use both `WEIGHTS` and `AGGREGATE` to calculate the weighted `MAX` score for each member.

```shell
dragonfly$> ZADD zset1 1 "apple" 6 "banana"
(integer) 2

dragonfly$> ZADD zset2 3 "apple" 4 "cherry"
(integer) 2

dragonfly$> ZUNION 2 zset1 zset2 WEIGHTS 2 3 AGGREGATE MAX WITHSCORES
1) "apple"
2) "9"        # max(1x2, 3x3) = 9
3) "banana"
4) "12"       # max(6x2, 0x3) = 12
5) "cherry"
6) "12"       # max(0x2, 4x3) = 12
```

In this example, weighted scores are calculated (`x2` for `zset1` and `x3` for `zset2`), and the maximum score is taken for each member during the union aggregation.

## Best Practices

- Use `WEIGHTS` when input sorted sets contribute unequally to the final result, such as giving more significance to scores from more recent activity.
- Choose the appropriate `AGGREGATE` method based on your use case.
  For example, `MIN` is useful for retaining the smallest score across sets, and `MAX` is good for ranking systems where the highest rank should dominate.

## Common Mistakes

- Assuming the result set will be sorted by member names.
  The returned members are sorted by their aggregated scores.

## FAQs

### What happens if some of the keys do not exist?

If a key does not exist, it is treated as an empty sorted set and does not affect the result.
For example, if `zset1` doesn't exist in the above examples, only `zset2`'s members will be used to compute the result.

### Can I use other aggregation methods besides `SUM`, `MIN`, or `MAX`?

No, `SUM`, `MIN`, and `MAX` are the only supported aggregation methods.
`SUM` is default if `AGGREGATE` is not specified.
