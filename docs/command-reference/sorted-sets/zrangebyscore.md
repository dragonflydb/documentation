---
description: Learn how to use the Redis ZRANGEBYSCORE command to return elements with scores within a given range in a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGEBYSCORE

<PageTitle title="Redis ZRANGEBYSCORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANGEBYSCORE` command is used to return all members in a sorted set with scores within the given range.
This command is particularly useful when working with time-series data, leaderboards, or prioritization algorithms.

## Syntax

```shell
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The name of the sorted set from which members will be retrieved.
- `min`: The minimum score for the range query.
- `max`: The maximum score for the range query.
- `WITHSCORES` (optional): If present, the command returns both members and their scores.
- `LIMIT offset count` (optional): Limits the number of results to `count` starting from the `offset`. Used for pagination.

## Return Values

The command returns an array of the members in the specified score range.
If `WITHSCORES` is provided, members and their scores are returned as alternating values in the array.

## Code Examples

### Basic Example

Return members with scores between `10` and `30` from a sorted set:

```shell
dragonfly> ZADD myzset 10 "a" 20 "b" 30 "c" 40 "d"
(integer) 4
dragonfly> ZRANGEBYSCORE myzset 10 30
1) "a"
2) "b"
3) "c"
```

### Using `WITHSCORES`

Retrieve members with scores between `10` and `30`, including the scores:

```shell
dragonfly> ZRANGEBYSCORE myzset 10 30 WITHSCORES
1) "a"
2) "10"
3) "b"
4) "20"
5) "c"
6) "30"
```

### Using `LIMIT`

Limit the result to 2 members, starting from the second one (`offset` = 1):

```shell
dragonfly> ZRANGEBYSCORE myzset 10 40 LIMIT 1 2
1) "b"
2) "c"
```

### Exclusive Ranges

You can use `(` to denote an open (exclusive) bound for the score range.
For example, only return members with scores greater than `10` but less than or equal to `30`:

```shell
dragonfly> ZRANGEBYSCORE myzset (10 30
1) "b"
2) "c"
```

## Best Practices

- Use `LIMIT` for pagination when dealing with large sets to reduce memory usage and improve performance.
- Combine `ZRANGEBYSCORE` with `WITHSCORES` to retrieve both the values and their scores in one command, providing better efficiency.

## Common Mistakes

- Misunderstanding that the `LIMIT` clause is applied after the score filtering, meaning it limits how many results are returned but does not affect the score range.
- Confusing `min` and `max` values: `min` must always be less than or equal to `max`.

## FAQs

### Can `ZRANGEBYSCORE` return members with equal scores?

Yes, if multiple members have the same score, all of them within the given score range will be returned.

### What happens if no members match the score range?

If no members fall within the specified score range, an empty array is returned.

### Can I specify negative infinity as a `min` or `max`?

Yes, `-inf` and `+inf` can be used as `min` and `max` respectively, allowing you to retrieve all members below or above certain score thresholds.
For example:

```shell
dragonfly> ZRANGEBYSCORE myzset -inf 20
1) "a"
2) "b"
```
