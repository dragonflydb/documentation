---
description: Learn to use the Redis BZPOPMIN command to remove and return the smallest score member from sorted sets, plus expert tips beyond the official doRedis docscs.
---

import PageTitle from '@site/src/components/PageTitle';

# BZPOPMIN

<PageTitle title="Redis BZPOPMIN Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BZPOPMIN` command is used to remove and return the member with the lowest score from one or more sorted sets.
This command is a blocking variant of `ZPOPMIN`, meaning it will block the client until a member is available to pop or until a specified timeout is reached.
It is commonly used in scenarios like task queues, where elements need to be processed in the order of priority (with the lowest score having the highest priority).

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

- If a member is successfully popped, the return is a three-element array: `[key, member, score]`, where:
  - `key`: The sorted set from which the element was popped.
  - `member`: The popped element.
  - `score`: The score of the popped element.
- If the timeout elapses without any elements being available, `nil` is returned.

## Code Examples

### Basic Example

Pop the element with the lowest score from a single sorted set with a 5-second timeout:

```shell
dragonfly> ZADD myzset 1 "task1" 2 "task2" 3 "task3"
(integer) 3
dragonfly> BZPOPMIN myzset 5
1) "myzset"
2) "task1"
3) "1"
```

### Blocking from Multiple Sorted Sets

Pop the element with the lowest score from any of two sorted sets, waiting for up to 3 seconds:

```shell
dragonfly> ZADD zset1 1 "a" 2 "b"
(integer) 2
dragonfly> ZADD zset2 3 "x" 4 "y"
(integer) 2
dragonfly> BZPOPMIN zset1 zset2 3
1) "zset1"
2) "a"
3) "1"
```

If more than one key has elements eligible to be popped, the one that provides the member with the lowest score is chosen first.

### Handling Timeouts

If none of the sorted sets contain any eligible elements within the given timeout period, the command will return `nil`:

```shell
dragonfly> BZPOPMIN zset1 zset2 1
(nil)
```

### Use Case in Task Queues

Imagine using sorted sets to manage tasks in a job queue, with each task having a priority (represented by its score).
Use `BZPOPMIN` to fetch the highest-priority task (the one with the lowest score):

```shell
dragonfly> ZADD task_queue 10 "low_priority_task" 5 "medium_priority_task" 1 "high_priority_task"
(integer) 3
dragonfly> BZPOPMIN task_queue 0
1) "task_queue"
2) "high_priority_task"
3) "1"
```

By blocking with a timeout of `0`, the system waits indefinitely until a task is available.

## Best Practices

- Use `BZPOPMIN` for scenarios where clients need to wait until a task or element becomes available in a priority queue.
  This prevents unnecessary polling of your sorted set.
- Opt for short timeouts when you need to periodically check conditions or implement timeouts on your own logic while still blocking.
- Leverage the command across multiple keys to handle collections of sorted sets without managing them independently.

## Common Mistakes

- Using the command without setting an appropriate timeout, such as setting it too high when the operation can affect client responsiveness.
- Confusing the `key` with the member of the sorted set.
  `BZPOPMIN` returns the key from which the member was popped, not just the member itself.

## FAQs

### What happens if all keys are empty?

If all the provided sorted sets are empty or don't exist, `BZPOPMIN` returns `nil` after the timeout elapses.

### Does the command work with negative timeouts?

No, the `timeout` parameter must be a non-negative integer or floating point value.
