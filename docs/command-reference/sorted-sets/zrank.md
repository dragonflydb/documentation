---
description: Learn how to use Redis' ZRANK command to find a member's index in a sorted set, with scores ordered low to high, plus expert tips beyond the official docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANK

<PageTitle title="Redis ZRANK Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANK` command is used to determine the rank or index of a member in a sorted set, ordered by the element's score in ascending order.
This command is particularly useful when you want to find the position of a specific element within a sorted set, such as ranking players in a leaderboard or keeping track of ordered items in a priority queue.

## Syntax

```shell
ZRANK key member
```

- **Time complexity:** O(log(N))
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set where the rank is to be determined.
- `member`: The member for which the rank is to be returned.

## Return Values

The command returns the rank (index) of the specified `member`.
The rank is a zero-based integer (starting from `0` for the member with the lowest score).
If the `member` does not exist in the set, `ZRANK` returns `nil`.

## Code Examples

### Basic Example: Determining Rank

Rank a player in a game's leaderboard:

```shell
dragonfly> ZADD leaderboard 5000 "Player1" 6000 "Player2" 7000 "Player3"
(integer) 3
dragonfly> ZRANK leaderboard "Player2"
(integer) 1
```

In the above example, `Player2` has a score of `6000` and ranks at index `1` in the sorted set.

### Non-existing Member

Attempt to retrieve the rank of a member that doesn't exist:

```shell
dragonfly> ZRANK leaderboard "Player4"
(nil)
```

Since `Player4` is not in the leaderboard, the command returns `nil`.

### Using `ZRANK` After Updating Scores

When a player's score changes, the rank will dynamically adjust:

```shell
dragonfly> ZADD leaderboard 8000 "Player2"
(integer) 0
dragonfly> ZRANK leaderboard "Player2"
(integer) 2
```

Here, `Player2`'s score was updated to `8000` and now ranks at index `2`.

### Retrieve Rank in Large Sorted Sets

For larger sets, `ZRANK` remains efficient and operates in logarithmic time complexity (`O(log(N))`):

```shell
dragonfly> ZADD large_set 1 "A" 2 "B" 3 "C" 4 "D" 5 "E"
(integer) 5
dragonfly> ZRANK large_set "D"
(integer) 3
```

Even with larger sets, you can quickly determine the rank of any member.

## Best Practices

- Use the `ZRANK` command to efficiently track ranks in real-time leaderboards and sorting systems.
- Pair `ZRANK` with other sorted set commands like `ZADD` and `ZREM` to maintain accurate and up-to-date rankings.

## Common Mistakes

- Not checking if a member exists before calling `ZRANK`, as it will return `nil` if the member is absent.
- Confusing the rank with the score. `ZRANK` does not return the score but rather the position of the member within the sorted set based on their score.

## FAQs

### Can I use `ZRANK` with descending order?

No, `ZRANK` only returns the rank in ascending order of scores.
To get the rank in descending order, use the related `ZREVRANK` command.

### What type is returned if the key does not represent a sorted set?

If the key exists but it does not hold a sorted set, `ZRANK` will return an error.

### What happens if the key does not exist?

If the key does not exist at all, `ZRANK` simply returns `nil`.
