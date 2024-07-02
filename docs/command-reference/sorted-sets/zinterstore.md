---
description: Learn how to use the Redis ZINTERSTORE command to intersect multiple sorted sets and store the result, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZINTERSTORE

<PageTitle title="Redis ZINTERSTORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ZINTERSTORE` is a Redis command used to compute the intersection of multiple sorted sets (zsets) and store the result in a new zset. This is particularly useful when you need to find common elements between different datasets while respecting their scores.

Typical scenarios include:

- Finding users who are active in multiple categories.
- Aggregating scores from different leaderboards.

## Syntax

```cli
ZINTERSTORE destination numkeys key [key ...] [WEIGHTS weight [weight ...]] [AGGREGATE SUM|MIN|MAX]
```

## Parameter Explanations

- `destination`: The name of the zset where the result will be stored.
- `numkeys`: The number of input zsets.
- `key [key ...]`: The keys of the input zsets.
- `WEIGHTS weight [weight ...]`: Optional. Specifies a multiplication factor for each input zset score. Default is 1.
- `AGGREGATE SUM|MIN|MAX`: Optional. Defines how to combine scores. Defaults to `SUM`.

## Return Values

The command returns an integer representing the number of elements in the resulting zset.

Example outputs:

- `(integer) 2`
- `(integer) 0`

## Code Examples

```cli
dragonfly> ZADD zset1 1 "a" 2 "b"
(integer) 2
dragonfly> ZADD zset2 1 "b" 2 "c"
(integer) 2
dragonfly> ZINTERSTORE out 2 zset1 zset2
(integer) 1
dragonfly> ZRANGE out 0 -1 WITHSCORES
1) "b"
2) "3"
```

## Best Practices

- Ensure all input zsets exist to avoid unexpected results.
- Use the `WEIGHTS` option to control the influence of each zset's scores in the final result.

## Common Mistakes

- Forgetting to specify `numkeys`, which leads to syntax errors.
- Misunderstanding the `AGGREGATE` parameter, which can cause incorrect score calculations if not set properly.

## FAQs

### What happens if one of the input zsets is empty?

The resulting zset will also be empty because there are no common elements.

### Can I use `ZINTERSTORE` with non-existent keys?

Yes, but non-existent keys are treated as empty sets, impacting the intersection result.
