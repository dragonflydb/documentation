---
description: Learn to use the Redis ZCOUNT command to count elements in a sorted set within a given score range, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZCOUNT

<PageTitle title="Redis ZCOUNT Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZCOUNT` command is used to count the members in a sorted set with scores within a specific range.
It allows you to quickly retrieve how many elements have scores between two given values, making it particularly useful for leaderboards, ranking systems, and range-based queries.

## Syntax

```shell
ZCOUNT key min max
```

- **Time complexity:** O(log(N)) with N being the number of elements in the sorted set.
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set whose members will be counted.
- `min`: The minimum score for the range.
- `max`: The maximum score for the range.

Both `min` and `max` can be:

- Exact numbers (e.g., `5`)
- `-inf` or `+inf` to represent negative or positive infinity, respectively
- Inclusive or exclusive bounds, where you prepend `(` to the value for exclusive comparisons (e.g., `(5` excludes score `5`).

## Return Values

- An integer representing the number of members in the sorted set that have scores within the specified range.
- If the key does not exist, `0` is returned.

## Code Examples

### Basic Example

Count all members with a score between `1` and `4`:

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4

dragonfly$> ZCOUNT myzset 1 4
(integer) 4
```

### Counting Exclusive Range

Count members where the score is between `1` (exclusive) and `4` (inclusive):

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4

dragonfly$> ZCOUNT myzset (1 4
(integer) 3
```

Count members where the score is between `1` (inclusive) and `4` (exclusive):

```shell
dragonfly$> ZCOUNT myzset 1 (4
(integer) 3
```


Count members where the score is between `1` and `4`, both exclusive:

```shell
dragonfly$> ZCOUNT myzset (1 (4
(integer) 2
```

### Using Negative and Positive Infinity

Count members without specifying an upper or lower bound using `-inf` and `+inf`:

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4

dragonfly$> ZCOUNT myzset -inf +inf
(integer) 4
```

## Best Practices

- When unsure of the score range, use `-inf` and `+inf` to include all members.
- Combine inclusive and exclusive bounds for precise member selection based on scores.

## Common Mistakes

- Using parentheses `(` incorrectly when specifying exclusive ranges. Always prepend `(` to the number for exclusivity.
- Forgetting that `min` and `max` refer to sorted set scores, not values.
- Reversing the order of `min` and `max` when specifying the range. If `min` is greater than `max`, the count will always be `0`.
- Assuming that `ZCOUNT` returns the elements themselves; it only returns the count.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZCOUNT` will return `0`, meaning there are no members to count.

### What’s the difference between `ZCOUNT` and `ZRANGE`?

While `ZCOUNT` returns the number of elements in a score range, [`ZRANGE`](zrange.md) returns the elements themselves.
If you only need the count, `ZCOUNT` is more efficient.
