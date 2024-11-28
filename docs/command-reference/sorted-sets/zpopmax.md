---
description: Learn how to use the Redis ZPOPMAX command to remove and return the member with the highest score in a sorted set, plus expert tips beyond the official docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZPOPMAX

<PageTitle title="Redis ZPOPMAX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZPOPMAX` command is used to remove and return the members with the highest scores in a sorted set.
This command is particularly useful when you need to implement a priority queue or retrieve the most important elements based on real-time scores.

## Syntax

```shell
ZPOPMAX key [count]
```

- **Time complexity:** O(log(N)\*M) with N being the number of elements in the sorted set, and M being the number of elements popped.
- **ACL categories:** @write, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set to pop the maximum scored elements.
- `count` (optional): The number of elements to pop. If not specified, it defaults to `1`.

## Return Values

- The command returns an array containing the popped elements and their scores.
- If the sorted set is empty or doesn't exist, the command returns an empty array.

## Code Examples

### Basic Example

Remove and return the member with the highest score from a sorted set:

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly$> ZPOPMAX myzset
1) "three"
2) "3"
```

### Popping Multiple Maximum Elements

Remove and return the top 2 members with the highest scores:

```shell
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4

dragonfly$> ZPOPMAX myzset 2
1) "four"
2) "4"
3) "three"
4) "3"
```

### Handling an Empty or Non-Existent Sorted Set

If the sorted set doesn't exist, `ZPOPMAX` will return an empty array:

```shell
dragonfly$> ZPOPMAX emptyset
(empty array)
```

## Best Practices

- Use `ZPOPMAX` when implementing stacks, priority queues, or leaderboard systems where you need to process or remove the highest priority items first.
- Be cautious when popping multiple elements (`count` parameter), as popping large amounts at once can lead to performance bottlenecks; consider batching wisely.

## Common Mistakes

- Using the command on a non-sorted set data structure will result in an error.
- Forgetting that when using `ZPOPMAX`, the members will be removed from the sorted set.
- Not considering the impact of popping multiple elements when performance is a concern.
  If your goal is to improve throughput, process smaller batches.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZPOPMAX` returns an empty array.

### What happens if the sorted set has fewer elements than `count`?

If the sorted set has fewer elements than the provided `count`,
`ZPOPMAX` will return all the available elements and remove them from the set.

### Can I use `ZPOPMAX` to atomically pop and process multiple items?

Yes, you can pass a `count` argument to pop multiple members atomically in a single call.
Keep in mind that members are returned in descending order of their scores.

### Can I use negative values for the `count` parameter?

No, `count` must always be a non-negative integer.
A negative value will result in an error.

### Does `ZPOPMAX` modify the sorted set?

Yes, `ZPOPMAX` removes the returned members from the set.
