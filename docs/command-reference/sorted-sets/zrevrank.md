---
description: Learn how to use Redis ZREVRANK to determine the index of a member in a sorted set, with scores ordered from high to low.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANK

<PageTitle title="Redis ZREVRANK Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREVRANK` command is used to determine the rank of a member in a sorted set, with the scores ordered from high to low.
The rank is counted starting from `0`, where `0` is the highest score.
This command is useful when you want to rank items such as user scores, product ratings, or leaderboard positions in descending order.

## Syntax

```shell
ZREVRANK key member
```

- **Time complexity:** O(log(N))
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set.
- `member`: The value whose rank you want to retrieve in the sorted set.

## Return Values

The command returns the rank of the member in the sorted set, with rank `0` being the highest.
If the member does not exist, the command returns `nil`.

## Code Examples

### Basic Example

Getting the reverse rank of a member in a sorted set:

```shell
dragonfly> ZADD leaderboard 100 "playerA" 200 "playerB" 150 "playerC"
(integer) 3
dragonfly> ZREVRANK leaderboard "playerB"
(integer) 0  # "playerB" has the highest score (200), so its rank is 0.
```

### Handling Non-Existent Members

When the specified member is not in the sorted set, `ZREVRANK` will return `nil`:

```shell
dragonfly> ZREVRANK leaderboard "playerD"
(nil)  # "playerD" does not exist in the set.
```

### Using `ZREVRANK` with Tied Scores

In case of identical scores, the order in which members were added is preserved:

```shell
dragonfly> ZADD leaderboard 100 "playerX" 100 "playerY"
(integer) 2
dragonfly> ZREVRANK leaderboard "playerX"
(integer) 2  # "playerX" was added before "playerY", so it has a higher rank.
dragonfly> ZREVRANK leaderboard "playerY"
(integer) 3  # "playerY" was added after "playerX", so it has a lower rank.
```

## Best Practices

- Use `ZREVRANK` when you need to retrieve ranks in descending order of scores.
  `ZREVRANK` is particularly useful for leaderboard systems where the highest score appears first.
- Combine `ZREVRANK` with `ZADD` for efficient ranking and scoring of members in real-time ranked systems, such as gaming leaderboards or top-performing products.

## Common Mistakes

- Assuming the rank is based on ascending order; `ZREVRANK` specifically orders elements from high to low.

- Forgetting that if the member does not exist, `ZREVRANK` will return `nil`, not an error or zero.

## FAQs

### What is the difference between `ZREVRANK` and `ZRANK`?

`ZREVRANK` gives the rank of the member with scores ordered from highest to lowest, while `ZRANK` gives the rank from lowest to highest.

### What happens if the key does not exist?

If the key does not exist, `ZREVRANK` will return `nil`.

### How is rank determined when two members have the same score?

When two members have the same score, the order in which the members were added is used to determine their rank.
Members added earlier will rank higher.
