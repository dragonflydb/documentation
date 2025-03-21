---
description: Learn how to use Redis ZUNIONSTORE command to apply set operations on sorted sets and store the resulting set in a new key.
---

import PageTitle from '@site/src/components/PageTitle';

# ZUNIONSTORE

<PageTitle title="Redis ZUNIONSTORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZUNIONSTORE` command is used to compute the union of multiple sorted sets and store the resulting sorted set in a new destination key.
It allows you to combine different sorted sets without modifying the original sets.
The union operation sums the scores of elements that are present in multiple input sets.
This command is useful for ranking systems, leaderboards, and other cases where you're dealing with multiple sorted scores across sets.

## Syntax

```shell
ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]]
  [AGGREGATE <SUM | MIN | MAX>]
```

- **Time complexity:** O(N)+O(M log(M)) with N being the sum of the sizes of the input sorted sets, and M being the number of elements in the resulting sorted set.
- **ACL categories:** @write, @sortedset, @slow

## Parameter Explanations

- `destination`: The key where the resulting sorted set will be stored. **If the key already exists, it is overwritten**.
- `numkeys`: The number of input sorted sets to consider for the union.
- `key`: The key(s) of the sorted sets to union.
- `WEIGHTS` (optional): A list of weights to multiply each sorted set's score before performing the union.
  If not provided, all weights default to `1`.
- `AGGREGATE` (optional): This defines how the resulting scores are computed when the same element appears in multiple sets.
  Options are `SUM` (default), `MIN`, or `MAX`.

## Return Values

- The command returns an integer indicating the number of elements in the resulting sorted set.

## Code Examples

### Basic Example

Union two sorted sets and store the result in a new key:

```shell
dragonfly$> ZADD zset1 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZADD zset2 1 "banana" 4 "date" 5 "elderberry"
(integer) 3

dragonfly$> ZUNIONSTORE result 2 zset1 zset2
(integer) 5

dragonfly$> ZRANGE result 0 -1 WITHSCORES
 1) "apple"
 2) "1"
 3) "banana"
 4) "3"
 5) "cherry"
 6) "3"
 7) "date"
 8) "4"
 9) "elderberry"
10) "5"
```

### Using `WEIGHTS` to Scale Scores

Use the `WEIGHTS` option to multiply scores before performing the union:

```shell
dragonfly$> ZADD zset1 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZADD zset2 1 "banana" 4 "date" 5 "elderberry"
(integer) 3

dragonfly$> ZUNIONSTORE result 2 zset1 zset2 WEIGHTS 2 3
(integer) 5

dragonfly$> ZRANGE result 0 -1 WITHSCORES
 1) "apple"
 2) "2"        # 1x2 + 0x3 = 2
 3) "cherry"
 4) "6"        # 3x2 + 0x3 = 6
 5) "banana"
 6) "7"        # 2x2 + 1x3 = 7
 7) "date"
 8) "12"       # 0x2 + 4x3 = 12
 9) "elderberry"
10) "15"       # 0x2 + 5x3 = 15
```

### Using `AGGREGATE` for Minimum or Maximum Scores

Use the `AGGREGATE` option to specify how to compute the final scores when an element exists in multiple sets:

```shell
dragonfly$> ZADD zset1 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZADD zset2 1 "banana" 4 "date" 5 "elderberry"
(integer) 3

# Using the MIN aggregation.
dragonfly$> ZUNIONSTORE result 2 zset1 zset2 AGGREGATE MIN
(integer) 5

dragonfly$> ZRANGE result 0 -1 WITHSCORES
 1) "apple"
 2) "1"
 3) "banana"
 4) "1"        # Minimum score for banana from both sorted sets.
 5) "cherry"
 6) "3"
 7) "date"
 8) "4"
 9) "elderberry"
10) "5"

# Using the MAX aggregation.
dragonfly$> ZUNIONSTORE result 2 zset1 zset2 AGGREGATE MAX
(integer) 5

dragonfly$> ZRANGE result 0 -1 WITHSCORES
 1) "apple"
 2) "1"
 3) "banana"
 4) "2"        # Maximum score for banana from both sorted sets.
 5) "cherry"
 6) "3"
 7) "date"
 8) "4"
 9) "elderberry"
10) "5"
```

## Best Practices

- Use the `WEIGHTS` option to apply different importance levels to each set in the union.
  This can be useful in ranking scenarios where certain sets carry more weight than others.
- The `AGGREGATE` option is especially helpful when you don't necessarily want to sum scores but need the minimum or maximum scores for shared elements across sets.

## Common Mistakes

- Omitting `numkeys`, which is mandatory, results in a syntax error.
  Always specify the number of input sets to union.
- Not providing enough keys based on the `numkeys` argument will cause an error.
  Ensure the correct number of keys match the `numkeys` specified.
- When using `WEIGHTS`, forgetting to provide enough weights for each input set will cause an error.
  Make sure the number of weights matches the number of input sets.

## FAQs

### What happens if one or more of the input sets do not exist?

If input sets do not exist, they are considered as empty sets.
No errors are raised in this case.

### Can I use `ZUNIONSTORE` for more than two sorted sets?

Yes, `ZUNIONSTORE` supports union of multiple sorted sets.
Simply adjust the `numkeys` parameter to reflect how many sets you are performing the union on, and provide the keys accordingly.

### Does `ZUNIONSTORE` modify the original sorted sets?

No, the input sorted sets remain unchanged.
The result is stored in a new set with the key you specify as the `destination`.
