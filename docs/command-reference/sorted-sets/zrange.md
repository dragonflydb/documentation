---
description: Learn to use the Redis ZRANGE command to fetch elements in a specific range from a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGE

<PageTitle title="Redis ZRANGE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANGE` command is used to retrieve a range of elements from a sorted set, **sorted by their score in ascending order (lowest to highest)**.
The `ZRANGE` command is highly useful when you are dealing with ordered data and need to fetch items within specific ranges of ranks or support paginated retrieval.

## Syntax

```shell
ZRANGE key start stop [BYSCORE | BYLEX] [REV] [LIMIT offset count] [WITHSCORES]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set.
- `start`: The starting index (zero-based) to retrieve elements.
   If negative, the index indicates an offset from the end of the set, with `-1` being the last element.
- `stop`: The ending index (zero-based) to retrieve elements.
  Similar to `start`, this can be negative to reference from the end of the set.
- `REV` (optional): If specified, the sorted set is traversed in reverse order (high-to-low scores).
- `LIMIT offset count` (optional): If specified, the command returns a subset of the elements within the specified range.
  - `offset`: The starting index of the subset (zero-based).
  - `count`: The number of elements to return. A negative `count` returns all elements from the `offset`.
- `WITHSCORES` (optional): If specified, the command returns the score of each element along with the element itself.

### Score Ranges with `BYSCORE`

When the `BYSCORE` option is provided, the command behaves like [`ZRANGEBYSCORE`](zrangebyscore.md)
and returns the range of elements from the sorted set having scores **equal or between** `start` and `stop`.

- When `BYSCORE` is used, the `start` and `stop` parameters are **treated as scores instead of indexes**.
- **By default, they are inclusive**. To make them exclusive, use the `(` character before the score.
- The `+inf` and `-inf` special values can be used to specify positive and negative infinity scores, respectively.

### Lexicographical Ranges with `BYLEX`

When the `BYLEX` option is provided, the command behaves like [`ZRANGEBYLEX`](zrangebylex.md)
and returns the range of elements from the sorted set within the **lexicographical closed range intervals**.

- When `BYLEX` is used, the `start` and `stop` parameters are **treated as lexicographical strings**.
- Valid `start` and `stop` values must start with `(` or `[` to indicate exclusive or inclusive bounds respectively.
- The `+` and `-` special values can be used to specify positive and negative infinity strings, respectively.

## Return Values

- The command returns an array of the elements in the specified sorted set range.
- If `WITHSCORES` is provided, the array contains each element followed by its score.

## Code Examples

### Basic Example

Retrieve a range of elements from a sorted set:

```shell
dragonfly$> ZADD myzset 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZRANGE myzset 0 -1
1) "apple"
2) "banana"
3) "cherry"
```

### Retrieve a Range with `WITHSCORES`

Get the elements and their associated scores from the sorted set `myzset`.

```shell
dragonfly$> ZADD myzset 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZRANGE myzset 0 -1 WITHSCORES
1) "apple"
2) "1"
3) "banana"
4) "2"
5) "cherry"
6) "3"
```

### Limiting the Results to a Specific Range

Get only the elements between the 1st and 2nd positions (indices 0-based):

```shell
dragonfly$> ZADD myzset 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZRANGE myzset 1 2
1) "banana"
2) "cherry"
```

### Using Negative Indexes

Retrieve the last two elements from the sorted set:

```shell
dragonfly$> ZADD myzset 1 "apple" 2 "banana" 3 "cherry"
(integer) 3

dragonfly$> ZRANGE myzset -2 -1
1) "banana"
2) "cherry"
```

### Using `ZRANGE` for Leaderboards

Assume you maintain a video game leaderboard sorted by player scores, which is an ideal use case for sorted sets:

```shell
dragonfly$> ZADD leaderboard 3500 "player1" 4200 "player2" 4800 "player3"
(integer) 3
```

Here, `ZRANGE` shows players sorted by their score in descending order using the `REV` option using an index range:

```shell
# Get the top 10 players with scores in descending order.
dragonfly$> ZRANGE leaderboard 0 9 WITHSCORES REV
1) "player3"
2) "4800"
3) "player2"
4) "4200"
5) "player1"
6) "3500"
```

You can also ask for players within a specific score range.
For example, to get players with 4200 < score <= 4800:

```shell
# With 'BYSCORE' option, get players with scores between 4800 (inclusive) and 4200 (exclusive).
dragonfly$> ZRANGE leaderboard 4800 (4200 BYSCORE WITHSCORES REV
1) "player3"
2) "4800"
```

If you don't know the exact high score, you can use `+inf` to represent positive infinity:

```shell
# Get players with scores greater than or equal to 4200.
dragonfly$> ZRANGE leaderboard +inf 4200 BYSCORE WITHSCORES REV
1) "player3"
2) "4800"
3) "player2"
4) "4200"
```

## Best Practices

- For reverse order (high-to-low scores), use the `REV` option or the [`ZREVRANGE`](zrevrange.md) command.
- Use `WITHSCORES` judiciously when scores matter to save bandwidth and processing time if scores are unnecessary.

## Common Mistakes

- Confusing positive and negative indexes—positive starts from `0` (beginning), while negative starts from `-1` (end).
- Using invalid ranges (`start` > `stop`) will always return an empty array.
- Misunderstanding that the `LIMIT` clause is applied after filtering, meaning it limits how many results are returned but does not affect the range.

## FAQs

### What happens if the given range is out of bounds?

`ZRANGE` will return the elements that are within the range.
If `start` is greater than `stop` or out of bounds, `ZRANGE` will return an empty array.

### What if the sorted set is empty?

If the sorted set is empty (or does not exist), `ZRANGE` will return an empty array.
