---
description: Learn how to use Redis ZREVRANGEBYSCORE command to retrieve members of a sorted set by score in descending order.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGEBYSCORE

<PageTitle title="Redis ZREVRANGEBYSCORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZREVRANGEBYSCORE` command in Redis is used to return a range of members in a sorted set, ordered from the highest to the lowest score. This command is particularly useful for scenarios like leaderboard systems, where you want to retrieve top-ranked items within specific score ranges.

## Syntax

```cli
ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **max**: The maximum score (inclusive) in the range to be queried.
- **min**: The minimum score (inclusive) in the range to be queried.
- **WITHSCORES**: Optional flag to include the scores of the returned elements.
- **LIMIT offset count**: Optional arguments to limit the number of elements returned, starting at the specified offset.

## Return Values

The command returns an array of members in the sorted set between the given scores, ordered from highest to lowest score. If `WITHSCORES` is specified, each member is followed by its score.

### Examples:

- Without `WITHSCORES`:

```cli
dragonfly> ZREVRANGEBYSCORE myzset 3 1
1) "two"
2) "one"
```

- With `WITHSCORES`:

```cli
dragonfly> ZREVRANGEBYSCORE myzset 3 1 WITHSCORES
1) "two"
2) "2"
3) "one"
4) "1"
```

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREVRANGEBYSCORE myzset 3 1
1) "three"
2) "two"
3) "one"
dragonfly> ZREVRANGEBYSCORE myzset 3 2 WITHSCORES
1) "three"
2) "3"
3) "two"
4) "2"
dragonfly> ZREVRANGEBYSCORE myzset 3 1 LIMIT 0 2
1) "three"
2) "two"
```

## Best Practices

- When using large sorted sets, consider utilizing the `LIMIT` option to paginate results and reduce memory overhead.
- Use `WITHSCORES` only when necessary to avoid additional processing time if scores are not needed.

## Common Mistakes

- Incorrectly specifying the `max` and `min` values can lead to unexpected results. Ensure that `max` is greater than or equal to `min`.
- Not considering the inclusive nature of the `max` and `min` parameters might cause confusion in the returned results.

## FAQs

### How does `ZREVRANGEBYSCORE` handle ties in scores?

When multiple members have the same score, they are returned in lexicographical order.

### Can I use negative infinity and positive infinity as scores?

Yes, you can use `+inf` and `-inf` to represent positive and negative infinity respectively when specifying score ranges.
