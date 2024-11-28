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
- `min` and `max`:
  - The minimum and maximum score values to filter the members.
  - **By default, they are inclusive**. To make them exclusive, use the `(` character before the score.
  - The `+inf` and `-inf` special values can be used to specify positive and negative infinity scores, respectively.
- `WITHSCORES` (optional): If present, the command returns both members and their scores.
- `LIMIT offset count` (optional): If specified, the command returns a subset of the elements within the specified range.
  - `offset`: The starting index of the subset (zero-based).
  - `count`: The number of elements to return. A negative `count` returns all elements from the `offset`.

## Return Values

- The command returns an array of the members in the specified score range.
- If `WITHSCORES` is provided, the array contains each element followed by its score.

## Code Examples

### Basic Example

Return members with scores between `10` and `30` from a sorted set:

```shell
dragonfly$> ZADD myzset 10 "a" 20 "b" 30 "c" 40 "d"
(integer) 4

dragonfly$> ZRANGEBYSCORE myzset 10 30
1) "a"
2) "b"
3) "c"
```

### Using `WITHSCORES`

Retrieve members with scores between `10` and `30`, including the scores:

```shell
dragonfly$> ZADD myzset 10 "a" 20 "b" 30 "c" 40 "d"
(integer) 4

dragonfly$> ZRANGEBYSCORE myzset 10 30 WITHSCORES
1) "a"
2) "10"
3) "b"
4) "20"
5) "c"
6) "30"
```

### Using `LIMIT`

Limit the result to 2 members (`count=2`), starting from the second one (`offset=1`):

```shell
dragonfly$> ZADD myzset 10 "a" 20 "b" 30 "c" 40 "d"
(integer) 4

dragonfly$> ZRANGEBYSCORE myzset 10 40 LIMIT 1 2
1) "b"
2) "c"
```

### Exclusive Ranges

You can use `(` to denote an open (exclusive) bound for the score range.
For example, only return members with scores greater than `10` but less than or equal to `30`:

```shell
dragonfly$> ZADD myzset 10 "a" 20 "b" 30 "c" 40 "d"
(integer) 4

dragonfly$> ZRANGEBYSCORE myzset (10 30
1) "b"
2) "c"
```

## Best Practices

- Take advantage of the `(` character to define exclusive score ranges.
- Use the `LIMIT` clause to avoid processing too many elements when you only need a subset of the range.
- If needed, combine `ZRANGEBYSCORE` with `WITHSCORES` to retrieve both the values and their scores in one command.

## Common Mistakes

- Using invalid ranges (`min` > `max`) will always return an empty array.
- Misunderstanding that the `LIMIT` clause is applied after filtering, meaning it limits how many results are returned but does not affect the score range.

## FAQs

### Can `ZRANGEBYSCORE` return members with equal scores?

Yes, if multiple members have the same score, all of them within the given score range will be returned.

### What happens if no members match the score range?

If no members fall within the specified score range, an empty array is returned.

### Can I specify infinite scores values?

Yes, `-inf` and `+inf` can be used as `min` and `max`, allowing you to retrieve all members below or above certain score thresholds.
For example:

```shell
dragonfly$> ZADD myzset 10 "a" 20 "b" 30 "c" 40 "d"
(integer) 4

dragonfly$> ZRANGEBYSCORE myzset -inf 20
1) "a"
2) "b"
```
