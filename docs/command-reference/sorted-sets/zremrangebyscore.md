---
description: Learn how to use Redis ZREMRANGEBYSCORE command to remove all members in a sorted set within the given scores.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYSCORE

<PageTitle title="Redis ZREMRANGEBYSCORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREMRANGEBYSCORE` command is used to remove all members from a sorted set that have a score within a given range.
This command is often used in scenarios where you need to efficiently prune entries in a sorted set based on their scores, such as removing expired sessions or data points from a leaderboard.

## Syntax

```shell
ZREMRANGEBYSCORE key min max
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.
- **ACL categories:** @write, @sortedset, @slow

## Parameter Explanations

- `key`: The name of the sorted set.
- `min`: The minimum score (inclusive) for the range. This can be a specific score or special values like `-inf` to denote negative infinity.
- `max`: The maximum score (inclusive) for the range. You can use values like `+inf` to include everything up to positive infinity.

## Return Values

The command returns the number of elements removed from the sorted set.

## Code Examples

### Basic Example

Remove members with scores between `1` and `3`:

```shell
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4
dragonfly> ZREMRANGEBYSCORE myzset 1 3
(integer) 3
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "four"
2) "4"
```

### Removing Members with Scores Below a Certain Value

Remove all members with scores less than `2`:

```shell
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4
dragonfly> ZREMRANGEBYSCORE myzset -inf 1
(integer) 1
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "two"
2) "2"
3) "three"
4) "3"
5) "four"
6) "4"
```

### Removing Members with Scores in a Floating-point Range

Use floating-point numbers to target a specific score range. In this case, remove members with scores between `2.5` and `4.5`:

```shell
dragonfly> ZADD myzset 2.5 "apple" 3.5 "banana" 1.5 "cherry"
(integer) 3
dragonfly> ZREMRANGEBYSCORE myzset 2.5 4.5
(integer) 2
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "cherry"
2) "1.5"
```

### Removing All Members Above a Certain Score

To remove all members with scores greater than `3.5`, use `+inf`:

```shell
dragonfly> ZADD myzset 2.5 "cat" 4 "dog" 6 "elephant"
(integer) 3
dragonfly> ZREMRANGEBYSCORE myzset 3.5 +inf
(integer) 2
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "cat"
2) "2.5"
```

## Best Practices

- Use `-inf` and `+inf` strategically to clear lower or upper bounds of the sorted set without hardcoding exact score ranges.
- If you need to maintain a capped sorted set based on scores (e.g., expiring items after a threshold), periodically use `ZREMRANGEBYSCORE`.

## Common Mistakes

- Forgetting that the score range is **inclusive**. If you mean to exclude the boundary value, you must use the special syntax of `(min` or `(max` to make the range exclusive.
- Trying to use non-numeric values for the `min` and `max` parameters; only valid floats, integers, and the special values `-inf` and `+inf` are allowed.

## FAQs

### Can I use exclusive ranges?

Yes, you can use parentheses to exclude a boundary from the range.
For example, `ZREMRANGEBYSCORE myzset (2 5` will remove all elements with scores greater than `2` but less than or equal to `5`.

### What happens if no elements fall within the score range?

If no elements in the sorted set fall within the provided score range, `ZREMRANGEBYSCORE` simply returns `0`, indicating that no elements were removed.

### Can the score range include negative values?

Yes, negative scores are allowed.
You can use negative values as both the `min` and `max` to define a valid range in the sorted set.
