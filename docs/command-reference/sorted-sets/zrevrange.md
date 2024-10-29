---
description: Learn how to use Redis ZREVRANGE command to return a range of members in a sorted set, by index, with scores ordered from high to low.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGE

<PageTitle title="Redis ZREVRANGE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREVRANGE` command is used to return a range of members in a sorted set, ordered from the highest to the lowest score.
It is the reverse of the `ZRANGE` command, which retrieves members in ascending order of their scores.
This command is particularly useful for ranking scenarios like leaderboards, where you want to list the top performers.

## Syntax

```shell
ZREVRANGE key start stop [WITHSCORES]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements returned.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set.
- `start`: The starting rank (0-based index), where `0` represents the highest score in the set.
- `stop`: The ending rank (inclusive).
- `WITHSCORES` (optional): If provided, the command returns both the member and its associated score.

## Return Values

- Without `WITHSCORES`, the command returns a list of members in the specified range, ordered from highest to lowest score.
- With `WITHSCORES`, the command returns a list where each member is followed by its score in the sorted set.

## Code Examples

### Basic Example

Retrieve the top 3 members of a leaderboard:

```shell
dragonfly> ZADD leaderboard 100 "PlayerA" 90 "PlayerB" 85 "PlayerC" 75 "PlayerD"
(integer) 4
dragonfly> ZREVRANGE leaderboard 0 2
1) "PlayerA"
2) "PlayerB"
3) "PlayerC"
```

### Using the `WITHSCORES` Option

Fetch the top 3 members along with their scores:

```shell
dragonfly> ZADD leaderboard 100 "PlayerA" 90 "PlayerB" 85 "PlayerC" 75 "PlayerD"
(integer) 4
dragonfly> ZREVRANGE leaderboard 0 2 WITHSCORES
1) "PlayerA"
2) "100"
3) "PlayerB"
4) "90"
5) "PlayerC"
6) "85"
```

### Specifying Negative Indexes

You can use negative indexes to fetch members starting from the end of the sorted set.
For example, to retrieve the last 2 members:

```shell
dragonfly> ZREVRANGE leaderboard -2 -1
1) "PlayerC"
2) "PlayerD"
```

### Example with a Full Leaderboard

Visualize an entire leaderboard for a game:

```shell
dragonfly> ZADD leaderboard 100 "PlayerA" 90 "PlayerB" 85 "PlayerC" 75 "PlayerD" 60 "PlayerE"
(integer) 5
dragonfly> ZREVRANGE leaderboard 0 -1
1) "PlayerA"
2) "PlayerB"
3) "PlayerC"
4) "PlayerD"
5) "PlayerE"
```

## Best Practices

- Use `ZREVRANGE` with `WITHSCORES` when you need both the members and their associated scores, especially in ranking applications.
- For leaderboards that might grow large over time, consider paginating results by adjusting the `start` and `stop` parameters dynamically.
- Whenever only member names are needed (and not scores), exclude the `WITHSCORES` option to optimize performance and reduce response size.

## Common Mistakes

- Confusing the `start` and `stop` parameters to be based on the score range rather than the index in the sorted set.
  They are 0-based positional indexes, not score values.
- Assuming that the command affects the sorting order or scores in the set.
  `ZREVRANGE` only retrieves the data and doesn't modify any existing scores or members.

## FAQs

### What happens if the key does not exist?

If the key doesn't exist, `ZREVRANGE` returns an empty list.

### Can I use `ZREVRANGE` with large datasets?

Yes.
However, it’s advised to use ranges (`start` and `stop`) to paginate through large sorted sets.
Fetching a large number of members at once could result in performance degradation.

### What happens if `start` or `stop` exceeds the set’s bounds?

If `start` or `stop` exceeds the sorted set's length, `ZREVRANGE` will return the elements within the valid range.
If there are no elements in the specified range, an empty list is returned.
