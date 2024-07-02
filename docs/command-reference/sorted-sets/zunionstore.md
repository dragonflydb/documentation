---
description: Learn how to use Redis ZUNIONSTORE command to apply set operations on sorted sets and store the resulting set in a new key.
---

import PageTitle from '@site/src/components/PageTitle';

# ZUNIONSTORE

<PageTitle title="Redis ZUNIONSTORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ZUNIONSTORE` is a Redis command used to compute the union of multiple sorted sets (zsets) and store the resulting sorted set in a new key. This command is especially useful when you need to aggregate or merge scores from different zsets, for example, combining user scores from different games into a single leaderboard.

## Syntax

```plaintext
ZUNIONSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
```

## Parameter Explanations

- `destination`: The key where the resulting sorted set will be stored.
- `numkeys`: The number of input sorted sets.
- `key [key ...]`: The keys of the input sorted sets.
- `WEIGHTS weight [weight ...]` (optional): Multipliers for each corresponding sorted set.
- `AGGREGATE SUM|MIN|MAX` (optional): Specifies how to aggregate scores from multiple sets (default is `SUM`).

## Return Values

The command returns an integer representing the number of elements in the resulting sorted set stored at the `destination` key.

## Code Examples

```cli
dragonfly> ZADD zset1 1 "one" 2 "two"
(integer) 2
dragonfly> ZADD zset2 2 "two" 3 "three"
(integer) 2
dragonfly> ZUNIONSTORE out 2 zset1 zset2
(integer) 3
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "one"
2) "1"
3) "three"
4) "3"
5) "two"
6) "4"
dragonfly> ZUNIONSTORE out 2 zset1 zset2 WEIGHTS 2 3
(integer) 3
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "one"
2) "2"
3) "two"
4) "10"
5) "three"
6) "9"
dragonfly> ZUNIONSTORE out 2 zset1 zset2 AGGREGATE MIN
(integer) 3
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "one"
2) "1"
3) "two"
4) "2"
5) "three"
6) "3"
```

## Best Practices

- Use the `WEIGHTS` option to normalize scores from different zsets if they have different scoring systems.
- Choose the appropriate `AGGREGATE` method (`SUM`, `MIN`, `MAX`) based on how you want to combine the scores from different sorted sets.

## Common Mistakes

- Forgetting to specify the correct `numkeys` value, which can lead to errors.
- Misordering the weights and keys when using the `WEIGHTS` option, causing incorrect results.

## FAQs

### What happens if a key does not exist?

If a specified key does not exist, it is treated as an empty sorted set, contributing no elements to the union.

### Can I use floating point numbers for scores with ZUNIONSTORE?

Yes, Redis supports floating-point numbers for scores in sorted sets.
