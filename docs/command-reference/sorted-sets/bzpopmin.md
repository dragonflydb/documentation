---
description: Learn to use the Redis BZPOPMIN command to remove and return the smallest score member from sorted sets, plus expert tips beyond the official doRedis docscs.
---

import PageTitle from '@site/src/components/PageTitle';

# BZPOPMIN

<PageTitle title="Redis BZPOPMIN Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BZPOPMIN` command is used to remove and return the member with the lowest score from one or more sorted sets.
This command is a blocking variant of [`ZPOPMIN`](zpopmin.md), meaning it will **block the connection for a specified timeout until a member is available to pop**.
It is commonly used in scenarios like task queues, where elements need to be processed in the order of priority (with the lowest score having the highest priority).
If multiple sorted sets are provided, `BZPOPMIN` will **pop from the first non-empty sorted set encountered in the order that the keys are given**.

## Syntax

```shell
BZPOPMIN key [key ...] timeout
```

- **Time complexity:** O(log(N)) with N being the number of elements in the sorted set.
- **ACL categories:** @write, @sortedset, @fast, @blocking

## Parameter Explanations

- `key [key ...]`: One or more keys pointing to sorted sets from which the minimum-scored element will be popped.
- `timeout`: The maximum time (in seconds) the client will block while waiting for an element before returning `nil`.
  If `timeout` is `0`, the command blocks indefinitely until a member is available.

## Return Values

The command returns a three-element array containing:

- The name of the sorted set that the element was popped from.
- The element with the lowest score.
- The score itself.

If the timeout expires without any elements to pop, `nil` is returned.

## Code Examples

### Basic Example

Pop the element with the lowest score from a single sorted set with a 5-second timeout:

```shell
dragonfly$> ZADD myzset 1 "task1" 2 "task2" 3 "task3"
(integer) 3
dragonfly$> BZPOPMIN myzset 5
1) "myzset"
2) "task1"
3) "1"
```

### Blocking from Multiple Sorted Sets

You can specify multiple sorted sets.
The command will act on the first non-empty set encountered:

```shell
dragonfly$> ZADD zset1 1 "a" 2 "b"
(integer) 2
dragonfly$> ZADD zset2 3 "x" 4 "y"
(integer) 2
dragonfly$> BZPOPMIN zset1 zset2 0
1) "zset1"
2) "a"
3) "1"
```

### Handling Timeouts

If none of the sorted sets contain any eligible elements within the given timeout period, the command will return `nil`:

```shell
dragonfly$> BZPOPMIN myzset 5
(nil)  # No elements in the sorted set, waited for 5 seconds and then returned nil.
```

### Use Case in Task Queues

Imagine using sorted sets to manage tasks in a job queue, with each task having a priority (represented by its score).
Use `BZPOPMIN` to fetch the highest-priority task (the one with the lowest score):

```shell
dragonfly$> ZADD task_queue 10 "low_priority_task" 5 "medium_priority_task" 1 "high_priority_task"
(integer) 3
dragonfly$> BZPOPMIN task_queue 0
1) "task_queue"
2) "high_priority_task"
3) "1"
```

By blocking with a timeout of `0`, the client connection waits indefinitely until a task is available.

## Best Practices

- Use `BZPOPMIN` for scenarios where clients need to wait until a task or element becomes available in a priority queue.
  This prevents unnecessary polling of your sorted set.
- Opt for short timeouts when you need to periodically check conditions or implement timeouts on your own logic while still blocking.
- Leverage the command across multiple keys to handle collections of sorted sets without managing them independently.

## Common Mistakes

- It can be easy to confuse the `timeout` parameter with `key` names if you're not careful with the syntax.
- Using the command without setting an appropriate `timeout`, such as setting it too high when the operation can affect client responsiveness.
- Confusing the key with the element of the sorted set in response.
  `BZPOPMIN` returns the key from which the member was popped as well, not just the member itself.

## FAQs

### What happens if the timeout is set to zero?

If the timeout is set to `0`, the connection will block indefinitely until a new element can be popped from the sorted set(s).

### Can I block on multiple sorted sets?

Yes, `BZPOPMIN` accepts multiple sorted set keys and will pop from the first non-empty sorted set, going through the list of keys from left to right, in the order they are provided.

### What happens if all keys are empty?

If all the provided sorted sets are empty or don't exist, `BZPOPMIN` returns `nil` after the timeout elapses.

### Does the command work with negative timeouts?

No, the `timeout` parameter must be a non-negative integer or floating point value specifying the maximum time in seconds to wait for an element to pop.
