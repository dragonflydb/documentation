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

- `key`: The key of the sorted set.
- `count` (optional): An integer specifying how many members with the lowest scores to pop. If omitted, the default value is `1`.

## Return Values

- If the `count` is `1` or not provided, the command returns a single array of two elements (the first is the member and the second is its score).
- If a `count` greater than `1` is specified, it returns an array with up to `count` elements, each being a two-element array of `[member, score]`.

## Code Examples

### Basic Example: Pop the member with the smallest score

In this example, we will insert a few members into a sorted set, and then we will use `ZPOPMIN` to remove and return the member with the smallest score.

```shell
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZPOPMIN myzset
1) "one"
2) "1"
```

The member `"one"` with the score "1" is returned and removed from the sorted set.

### Pop multiple members with the smallest scores

You can also specify a `count` to remove and return multiple members with the smallest scores.
This can be useful in scenarios where you need to process more than one item at a time.

```shell
dragonfly> ZADD myzset 4 "four" 5 "five" 6 "six"
(integer) 3
dragonfly> ZPOPMIN myzset 2
1) "two"
2) "2"
3) "three"
4) "3"
```

The members `"two"` and `"three"` are both returned, as they had the two smallest scores, and they are removed from the set.

### Using `ZPOPMIN` in real-time ranking systems

Imagine you are implementing a ranking system for a game, and you frequently need to pop the lowest-ranked player for removal or recalculations.

```shell
dragonfly> ZADD leaderboard 1000 "playerA" 1200 "playerB" 1500 "playerC"
(integer) 3
dragonfly> ZPOPMIN leaderboard
1) "playerA"
2) "1000"
```

In this case, `"playerA"` with the score of 1000 is returned and removed, as they were the lowest-ranked player.

### Popping from an empty sorted set

If the sorted set is empty, `ZPOPMIN` returns `nil`:

```shell
dragonfly> ZPOPMIN emptyset
(nil)
```

## Best Practices

- Use `ZPOPMIN` to maintain performance in real-time systems where you need to process the lowest-scored items first, such as in event queues or job prioritization systems.
- If you frequently need to remove more than one item, specify the `count` parameter to batch multiple removals in a single atomic operation.

## Common Mistakes

- Assuming `ZPOPMIN` operates on unordered sets; it works only with sorted sets.
- Forgetting that when using `ZPOPMIN`, the members will be permanently removed from the sorted set.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZPOPMIN` returns `nil`, as there are no members to pop.

### Can I use `ZPOPMIN` to atomically pop and process multiple items?

Yes, you can pass a `count` argument to pop multiple members atomically in a single call.
Keep in mind that members are returned in ascending order of their scores.

### Will `ZPOPMIN` return ties if multiple members have the same score?

Yes, if multiple members have the same score, `ZPOPMIN` will return them in lexicographical order.
For example, if two or more members have an identical score, the one that comes first alphabetically will be returned first.
