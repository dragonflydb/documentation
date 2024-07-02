---
description: Learn how to use Redis ZUNION command to perform a union of multiple sorted sets, getting the sorted set of unique elements.
---

import PageTitle from '@site/src/components/PageTitle';

# ZUNION

<PageTitle title="Redis ZUNION Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZUNION` command is used to perform the union of multiple sorted sets in Redis. It aggregates the scores of elements from the provided sets and adds them into a new sorted set. This command is typically used when you need to combine sorted sets for leaderboard applications or to aggregate data from different sources.

## Syntax

```plaintext
ZUNION numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
```

## Parameter Explanations

- **numkeys**: The number of keys to be combined.
- **key [key ...]**: The list of keys representing the sorted sets to be united.
- **WEIGHTS weight [weight ...]**: Optional. Modifies the score of each element in the sorted sets by multiplying it with this factor.
- **AGGREGATE SUM|MIN|MAX**: Optional. Specifies how the results should be aggregated. By default, it's `SUM`.
  - `SUM`: Adds up all the scores (default).
  - `MIN`: Takes the minimum score.
  - `MAX`: Takes the maximum score.

## Return Values

The `ZUNION` command returns an array of elements with their scores from the resulting union of the input sorted sets.

Example outputs:

```plaintext
1) "member1"
2) "2.0"
3) "member2"
4) "3.5"
```

## Code Examples

```cli
dragonfly> ZADD zset1 1 "one"
(integer) 1
dragonfly> ZADD zset1 2 "two"
(integer) 1
dragonfly> ZADD zset2 1 "one"
(integer) 1
dragonfly> ZADD zset2 3 "three"
(integer) 1
dragonfly> ZUNION 2 zset1 zset2
1) "one"
2) "2.0"
3) "two"
4) "2.0"
5) "three"
6) "3.0"
dragonfly> ZUNION 2 zset1 zset2 WEIGHTS 2 3
1) "one"
2) "5.0"
3) "two"
4) "4.0"
5) "three"
6) "9.0"
dragonfly> ZUNION 2 zset1 zset2 AGGREGATE MAX
1) "one"
2) "1.0"
3) "two"
4) "2.0"
5) "three"
6) "3.0"
```

## Best Practices

- Ensure the `numkeys` parameter accurately matches the number of keys provided.
- Use the `WEIGHTS` option to adjust the significance of each sorted set based on your application requirements.
- Choose the appropriate `AGGREGATE` option (`SUM`, `MIN`, `MAX`) to get the desired result based on how you want to combine the scores.

## Common Mistakes

- Miscounting the `numkeys` parameter, leading to incorrect command execution.
- Forgetting that `WEIGHTS` and `AGGREGATE` options are optional but can significantly change the output if not properly understood.

## FAQs

### What happens if the same member exists in multiple sets?

If the same member exists in multiple sets, its score will be aggregated based on the specified `AGGREGATE` option. By default, scores are summed.

### Can I use `ZUNION` with only one sorted set?

Yes, but it would be equivalent to just copying the sorted set since there’s no other set to union with.

### How does `WEIGHTS` affect the result?

The `WEIGHTS` option multiplies the score of each element in the sorted sets by the provided weight, allowing for weighted unions.
