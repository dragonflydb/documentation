---
description: Learn how to use Redis ZREVRANK to determine the index of a member in a sorted set, with scores ordered from high to low.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANK

<PageTitle title="Redis ZREVRANK Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREVRANK` command is used to determine the rank of a member in a sorted set, **with the scores ordered from high to low**.
The rank is counted starting from `0`, where `0` is the highest score.
This command is useful when you want to rank items such as user scores or product ratings in descending order.

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

- The command returns the rank of the member in the sorted set, with rank `0` being the highest.
- If the member does not exist, the command returns `nil`.

## Code Examples

### Basic Example

Getting the reverse rank of a member in a sorted set:

```shell
dragonfly$> ZADD leaderboard 100 "PlayerA" 200 "PlayerB" 150 "PlayerC"
(integer) 3

dragonfly$> ZREVRANK leaderboard "PlayerB"
(integer) 0  # PlayerB has the highest score, so its rank is 0.
```

### Handling Non-Existent Members

When the specified member is not in the sorted set, `ZREVRANK` will return `nil`:

```shell
dragonfly$> ZADD leaderboard 100 "PlayerA" 200 "PlayerB" 150 "PlayerC"
(integer) 3

dragonfly$> ZREVRANK leaderboard "PlayerD"
(nil)  # PlayerD does not exist in the sorted set.
```

## Best Practices

- Use `ZREVRANK` when you need to retrieve ranks in descending order of scores.
  `ZREVRANK` is particularly useful for leaderboard systems where the highest score appears first.
- Combine `ZREVRANK` with [`ZADD`](zadd.md) for efficient ranking and scoring of members in real-time ranked systems, such as gaming leaderboards or top-performing products.

## Common Mistakes

- Assuming the rank is based on ascending order. `ZREVRANK` specifically orders elements from high to low.
- Forgetting that if the member does not exist, `ZREVRANK` will return `nil`, not an error or zero.

## FAQs

### What is the difference between `ZREVRANK` and `ZRANK`?

`ZREVRANK` gives the rank of the member with scores ordered from highest to lowest, while [`ZRANK`](zrank.md) gives the rank from lowest to highest.

### What happens if the key does not exist?

If the key does not exist, `ZREVRANK` will return `nil`.
