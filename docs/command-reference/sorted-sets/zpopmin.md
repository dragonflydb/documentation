---
description: Learn how to use the Redis ZPOPMIN command to remove and return the member with the lowest score in a sorted set, plus expert tips beyond the official docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZPOPMIN

<PageTitle title="Redis ZPOPMIN Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZPOPMIN` command is used to remove and return the member with the smallest score in a sorted set.
Sorted sets are particularly useful when you need to maintain ranking systems or work with ordered collections.
With `ZPOPMIN`, you can efficiently extract the lowest-ranked item along with its score.

## Syntax

```shell
ZPOPMIN key [count]
```

- **Time complexity:** O(log(N)\*M) with N being the number of elements in the sorted set, and M being the number of elements popped.
- **ACL categories:** @write, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set to pop the minimum scored elements.
- `count` (optional): The number of elements to pop. If not specified, it defaults to `1`.

## Return Values

- The command returns an array containing the popped elements and their scores.
- If the sorted set is empty or doesn't exist, the command returns an empty array.

## Code Examples

### Basic Example

In this example, we will insert a few members into a sorted set, and then we will use `ZPOPMIN` to remove and return the member with the smallest score.

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly$> ZPOPMIN myzset
1) "one"
2) "1"
```

The member `"one"` with the score "1" is returned and removed from the sorted set.

### Pop multiple members with the smallest scores

You can also specify a `count` to remove and return multiple members with the smallest scores.
This can be useful in scenarios where you need to process more than one item at a time.

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly$> ZPOPMIN myzset 2
1) "one"
2) "1"
3) "two"
4) "2"
```

The members `"one"` and `"two"` are both returned, as they had the two smallest scores, and they are removed from the set.

### Using `ZPOPMIN` in Real-Time Ranking Systems

Imagine you are implementing a ranking system for a game, and you frequently need to pop the lowest-ranked player for removal or recalculations.

```shell
dragonfly$> ZADD leaderboard 1000 "playerA" 1200 "playerB" 1500 "playerC"
(integer) 3

dragonfly$> ZPOPMIN leaderboard
1) "playerA"
2) "1000"
```

In this case, `"playerA"` with the score of 1000 is returned and removed, as they were the lowest-ranked player.

### Handling an Empty or Non-Existent Sorted Set

If the sorted set doesn't exist, `ZPOPMIN` will return an empty array:

```shell
dragonfly$> ZPOPMIN emptyset
(empty array)
```

## Best Practices

- Use `ZPOPMIN` to maintain performance in real-time systems where you need to process the lowest-scored items first, such as in event queues or job prioritization systems.
- If you frequently need to remove more than one item, specify the `count` parameter to batch multiple removals in a single atomic operation.

## Common Mistakes

- Using the command on a non-sorted set data structure will result in an error.
- Forgetting that when using `ZPOPMIN`, the members will be removed from the sorted set.
- Not considering the impact of popping multiple elements when performance is a concern.
  If your goal is to improve throughput, process smaller batches.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZPOPMIN` returns an empty array.

### What happens if the sorted set has fewer elements than `count`?

If the sorted set has fewer elements than the provided `count`,
`ZPOPMIN` will return all the available elements and remove them from the set.

### Can I use `ZPOPMIN` to atomically pop and process multiple items?

Yes, you can pass a `count` argument to pop multiple members atomically in a single call.
Keep in mind that members are returned in ascending order of their scores.

### Can I use negative values for the `count` parameter?

No, `count` must always be a non-negative integer.
A negative value will result in an error.

### Does `ZPOPMIN` modify the sorted set?

Yes, `ZPOPMIN` removes the returned members from the set.
