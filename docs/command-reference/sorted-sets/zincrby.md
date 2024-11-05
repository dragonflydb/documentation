---
description: Learn to use the Redis ZINCRBY command to increment the score of a member in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZINCRBY

<PageTitle title="Redis ZINCRBY Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZINCRBY` command is used to increment the score of a member in a sorted set (zset).
If the member doesn't exist, it is added with the incremented score as its initial value.
This command is often used in leaderboard systems, statistical counters, and ranking applications where member scores need to be dynamically updated.

## Syntax

```shell
ZINCRBY key increment member
```

- **Time complexity:** O(log(N)) where N is the number of elements in the sorted set.
- **ACL categories:** @write, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set whose member's score is to be incremented.
- `increment`: The value by which to increment the member's score.
  The increment can be an integer or a floating-point number.
- `member`: The member whose score will be incremented.
  If the member does not exist, it is added to the sorted set.

## Return Values

The command returns the new score of the member after being incremented.

## Code Examples

### Basic Example

Increment the score of a member and return the updated score:

```shell
# Initially, user123 has a score of 10 in the leaderboard.
dragonfly$> ZADD leaderboard 10 user123
(integer) 1
# Increment user123's score by 5.
dragonfly$> ZINCRBY leaderboard 5 user123
"15"
```

### Adding a New Member with `ZINCRBY`

If the member doesn't exist, `ZINCRBY` adds it with the increment as its initial score:

```shell
# user999 doesn't exist in the sorted set yet.
dragonfly$> ZINCRBY leaderboard 8 user999
"8"
# Now user999 has a score of 8.
```

### Increment a Member Score with a Negative Value

Use a negative increment to reduce the member's score:

```shell
# user123 currently has a score of 15 in the leaderboard.
dragonfly$> ZINCRBY leaderboard -3 user123
"12"  # The score is now 12 after applying the negative increment.
```

### Floating-Point Increments

You can use floating-point values for finer score adjustments:

```shell
# user456 has no score yet and will be created with a floating-point score.
dragonfly$> ZINCRBY leaderboard 2.5 user456
"2.5"
# Further increment using a floating-point value.
dragonfly$> ZINCRBY leaderboard 0.1 user456
"2.6"
```

## Best Practices

- Use `ZINCRBY` efficiently in score-aggregation scenarios such as updating user points, wins, or other rank-based updates.
- When using floating-point increments, consider precision requirements for your application to avoid rounding issues.

## Common Mistakes

- Using `ZINCRBY` on a key that doesn't store a sorted set will result in an error.
  Always ensure the key references a valid sorted set.
- Expecting `ZINCRBY` to work on non-numeric values will lead to errors, as it only supports numeric increments.

## FAQs

### Can I decrement a score with `ZINCRBY`?

Yes, by providing a negative increment value, you can reduce the score of a member.

### What happens if the key doesn't exist?

If the key doesn't exist, a new sorted set is created, and the member is added with the provided increment as its initial score.

### What if the member doesn't exist in the sorted set?

If the member doesn't exist, it will be added to the sorted set with the provided increment as its initial score.
