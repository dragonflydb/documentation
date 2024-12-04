---
description: Learn how to use Redis ZREVRANGEBYSCORE command to retrieve members of a sorted set by score in descending order.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGEBYSCORE

<PageTitle title="Redis ZREVRANGEBYSCORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREVRANGEBYSCORE` command is used to retrieve members from a sorted set whose score falls within a specified range, ordered from the highest to the lowest score.
This command is commonly used when you need sorted results based on a score but in descending order, making it ideal for tasks like leaderboard applications, event tracking, or prioritization systems.

## Syntax

```shell
ZREVRANGEBYSCORE key max min [WITHSCORES] [LIMIT offset count]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key identifying the sorted set.
- `max` and `min`:
    - The maximum and minimum score values to filter the members to be removed.
    - **By default, they are inclusive**. To make them exclusive, use the `(` character before the score.
    - The `+inf` and `-inf` special values can be used to specify positive and negative infinity scores, respectively.
- `WITHSCORES` (optional): If provided, the command includes the scores of the returned members.
- `LIMIT offset count` (optional): Limits the number of elements returned. `offset` specifies how many elements to skip, and `count` specifies the maximum number of elements to return.

## Return Values

- The command returns an array of members within the score range, ordered from the highest to the lowest score.
- If `WITHSCORES` is used, the returned array includes both members and their scores as alternating elements.

## Code Examples

### Basic Example

Retrieve the members in a sorted set with scores between `50` and `0` inclusive, ordered from highest to lowest:

```shell
dragonfly$> ZADD leaderboard 50 "Alice" 100 "Bob" 25 "Charlie" 75 "Dana"
(integer) 4

dragonfly$> ZREVRANGEBYSCORE leaderboard 50 0
1) "Alice"
2) "Charlie"
```

### Using `WITHSCORES`

Retrieve the members and their scores between `50` and `0` inclusive:

```shell
dragonfly$> ZADD leaderboard 50 "Alice" 100 "Bob" 25 "Charlie" 75 "Dana"
(integer) 4

dragonfly$> ZREVRANGEBYSCORE leaderboard 50 0 WITHSCORES
1) "Alice"
2) "50"
3) "Charlie"
4) "25"
```

### Limiting Results with `LIMIT`

Retrieve up to two members from the sorted set with scores between `100` and `0`, skipping the first element (`offset=1`):

```shell
dragonfly$> ZADD leaderboard 50 "Alice" 100 "Bob" 25 "Charlie" 75 "Dana"
(integer) 4

dragonfly$> ZREVRANGEBYSCORE leaderboard 100 0 WITHSCORES LIMIT 1 2
1) "Dana"
2) "75"
3) "Alice"
4) "50"
```

### Using Exclusive Ranges

Use parentheses to represent exclusive ranges.
For example, retrieve members with scores between `100` (exclusive) and `50` (inclusive):

```shell
dragonfly$> ZADD leaderboard 50 "Alice" 100 "Bob" 25 "Charlie" 75 "Dana"
(integer) 4

dragonfly$> ZREVRANGEBYSCORE leaderboard (100 50 WITHSCORES
1) "Dana"
2) "75"
3) "Alice"
4) "50"
```

### Using Special Values

Retrieve members with scores between `+inf` and `50`:

```shell
dragonfly$> ZADD leaderboard 50 "Alice" 100 "Bob" 25 "Charlie" 75 "Dana"
(integer) 4

dragonfly$> ZREVRANGEBYSCORE leaderboard +inf 50 WITHSCORES
1) "Bob"
2) "100"
3) "Dana"
4) "75"
5) "Alice"
6) "50"
```

## Best Practices

- Use `WITHSCORES` when you need not only the members but also their associated scores. This is particularly useful in leaderboard applications.
- Combine `LIMIT` with score ranges to implement efficient pagination in systems that need ranked results without retrieving the entire set.
- Consider using exclusive ranges with `(` for more advanced querying when exact scores should be excluded from results.

## Common Mistakes

- Confusing the order in which `ZREVRANGEBYSCORE` returns results. This command returns members from highest to lowest score, opposite of [`ZRANGEBYSCORE`](zrangebyscore.md).
- Using `LIMIT` without considering its interaction with the range scope. Remember that `LIMIT` works on the result after sorting in score order.
- Forgetting that both `max` and `min` are both inclusive by default unless prefixed with `(` for exclusive ranges.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZREVRANGEBYSCORE` returns an empty array.

### Can I use floating-point numbers for `min` and `max`?

Yes, both integer and floating-point numbers are supported for sorted set scores.

### What is the difference between `ZRANGEBYSCORE` and `ZREVRANGEBYSCORE`?

[`ZRANGEBYSCORE`](zrangebyscore.md) returns members sorted by increasing score (lowest to highest), while `ZREVRANGEBYSCORE` returns them in descending order (highest to lowest).
