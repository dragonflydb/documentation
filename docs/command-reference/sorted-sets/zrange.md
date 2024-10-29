---
description: Learn to use the Redis ZRANGE command to fetch elements in a specific range from a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGE

<PageTitle title="Redis ZRANGE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANGE` command is used to retrieve a range of elements from a sorted set, sorted by their score in ascending order (lowest to highest).
The `ZRANGE` command is highly useful when you are dealing with ordered data and need to fetch items within specific ranges of ranks or support paginated retrieval.

## Syntax

```shell
ZRANGE key start stop [WITHSCORES]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set.
- `start`: The starting index to retrieve elements.
  Indexes can be either positive (from the beginning) or negative (from the end of the set).
- `stop`: The ending index to retrieve elements.
  Similar to `start`, this can be negative to reference from the end of the set.
- `WITHSCORES` (optional): If specified, the command returns the score of each element along with the element itself.

## Return Values

The command returns an array of the elements in the specified sorted set range.
If `WITHSCORES` is provided, the array contains each element followed by its score.

## Code Examples

### Basic Example

Retrieve a range of elements from a sorted set:

```shell
dragonfly> ZADD myzset 1 "apple" 2 "banana" 3 "cherry"
(integer) 3
dragonfly> ZRANGE myzset 0 -1
1) "apple"
2) "banana"
3) "cherry"
```

### Retrieve a Range with `WITHSCORES`

Get the elements and their associated scores from the sorted set `myzset`.

```shell
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
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
dragonfly> ZRANGE myzset 1 2
1) "banana"
2) "cherry"
```

### Using Negative Indexes

Retrieve the last two elements from the sorted set:

```shell
dragonfly> ZRANGE myzset -2 -1
1) "banana"
2) "cherry"
```

### Using `ZRANGE` for Leaderboards

Assume you maintain a video game leaderboard sorted by player scores.
Players on this leaderboard are stored in a sorted set, where the score is their points:

```shell
dragonfly> ZADD leaderboard 3500 "player1" 4200 "player2" 4800 "player3"
(integer) 3
dragonfly> ZRANGE leaderboard 0 -1 WITHSCORES
1) "player1"
2) "3500"
3) "player2"
4) "4200"
5) "player3"
6) "4800"
```

Here, `ZRANGE` helps you show players sorted by their rank, with an option to include or omit their scores.

## Best Practices

- If you want an efficient paginated ranked list, use `ZRANGE` with start/stop parameters to move across the sorted set.
- For reverse order (high-to-low scores), use `ZREVRANGE` instead.
- Use `WITHSCORES` judiciously when scores matter to save bandwidth and processing time if scores are unnecessary.

## Common Mistakes

- Confusing positive and negative indexes — positive starts from `0` (beginning), while negative starts from `-1` (end).
- Expecting `ZRANGE` to return ranks; it only returns the elements and optionally the scores.
- Using invalid ranges (`start` > `stop`) will return an empty array.

## FAQs

### What happens if the given range is out of bounds?

`ZRANGE` will return the elements that are within the range.
If `start` is greater than `stop` or out of bounds, it will return an empty array.

### Can I fetch elements sorted by their score in descending order?

No, `ZRANGE` provides elements sorted by ascending score.
To retrieve items in descending order, use `ZREVRANGE`.

### What if the sorted set is empty?

If the sorted set is empty (or does not exist), `ZRANGE` will return an empty array.
