---
description: Learn how to use Redis ZREMRANGEBYRANK command to remove all members in a sorted set within the given indexes.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYRANK

<PageTitle title="Redis ZREMRANGEBYRANK Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREMRANGEBYRANK` command is used to remove members from a sorted set based on their rank.
The rank is the position of a member in the sorted set, with 0 being the rank of the lowest-scored member.
This command is useful when you need to prune elements within a certain rank range, such as when implementing leaderboard cleanups or time-based sliding windows.

## Syntax

```shell
ZREMRANGEBYRANK key start stop
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.
- **ACL categories:** @write, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set where members will be removed.
- `start`: The starting rank from where removals should begin (inclusive).
- `stop`: The ending rank for removals (inclusive).

## Return Values

This command returns an integer representing the number of members that were removed from the sorted set.

## Code Examples

### Basic Example: Remove by Rank

Remove the members ranked between 0 (the first rank) and 1 (the second rank) in a sorted set:

```shell
dragonfly> ZADD leaderboard 100 "Alice" 150 "Bob" 200 "Charlie"
(integer) 3
dragonfly> ZREMRANGEBYRANK leaderboard 0 1
(integer) 2
dragonfly> ZRANGE leaderboard 0 -1
1) "Charlie"
```

### Example with Full Range Removal

Remove all members from a sorted set by specifying the entire range:

```shell
dragonfly> ZADD players 120 "Player1" 140 "Player2" 160 "Player3"
(integer) 3
dragonfly> ZREMRANGEBYRANK players 0 -1
(integer) 3
dragonfly> ZRANGE players 0 -1
(empty array)
```

### Remove Last Two Members Based on Rank

Remove the last two members from the sorted set using negative ranks:

```shell
dragonfly> ZADD scores 300 "u1" 400 "u2" 500 "u3" 600 "u4"
(integer) 4
dragonfly> ZREMRANGEBYRANK scores -2 -1
(integer) 2
dragonfly> ZRANGE scores 0 -1
1) "u1"
2) "u2"
```

## Best Practices

- `ZREMRANGEBYRANK` efficiently removes elements by rank without having to retrieve them first, making it particularly useful for cleaning up large datasets.
- If you need to remove based on score instead of rank, consider using `ZREMRANGEBYSCORE`.

## Common Mistakes

- Misunderstanding that the rank is based on the position of the member in the sorted set, not the score. For rank-based removal, always use `ZREMRANGEBYRANK`, not `ZREMRANGEBYSCORE`.
- Providing a `start` or `stop` rank that is out of bounds. This doesn't cause an error but will result in no elements being removed.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZREMRANGEBYRANK` simply returns `0` because there are no members to remove.

### Can I use negative ranks?

Yes, negative ranks can be used to refer to elements starting from the end of the sorted set.
For example, `-1` refers to the last element, `-2` to the second last, and so on.
This is particularly useful for trimming the sorted set without knowing its exact length.
