---
description: Learn how to use the Redis BZPOPMAX command to remove and return the highest score member from sorted sets, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# BZPOPMAX

<PageTitle title="Redis BZPOPMAX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BZPOPMAX` command is used to remove and return the member with the highest score in a sorted set.
This command is a blocking variant of [`ZPOPMAX`](zpopmax.md), meaning it will **block the connection for a specified timeout until a member is available to pop**.
This makes it particularly useful for creating delayed or sorted workflows such as job queues where items with the highest priority need to be processed first.
If multiple sorted sets are provided, `BZPOPMAX` will **pop from the first non-empty sorted set encountered in the order that the keys are given**.

## Syntax

```shell
BZPOPMAX key [key ...] timeout
```

- **Time complexity:** O(log(N)) with N being the number of elements in the sorted set.
- **ACL categories:** @write, @sortedset, @fast, @blocking

## Parameter Explanations

- `key`: One or more keys, each representing a sorted set.
- `timeout`: The maximum number of seconds to wait if all the provided sorted sets are empty. A `0` timeout means to block indefinitely until an element is available to pop.

## Return Values

The command returns a three-element array containing:

- The name of the sorted set that the element was popped from.
- The element with the highest score.
- The score itself.

If the timeout expires without any elements to pop, `nil` is returned.

## Code Examples

### Basic Example

Pop the highest score element from a sorted set:

```shell
dragonfly$> ZADD myzset 1 "item1" 2 "item2" 3 "item3"
(integer) 3

dragonfly$> BZPOPMAX myzset 0
1) "myzset"
2) "item3"
3) "3"
```

### Blocking for Elements

If the sorted set is empty, `BZPOPMAX` will wait for new elements or until the timeout:

```shell
dragonfly$> ZADD myzset 1 "item1" 2 "item2"
(integer) 2

dragonfly$> ZPOPMAX myzset
1) "item2"
2) "2"

dragonfly$> ZPOPMAX myzset
1) "item1"
2) "1"

dragonfly$> BZPOPMAX myzset 5
(nil)  # No elements in the sorted set, waited for 5 seconds and then returned nil.
```

### Using Multiple Keys

You can specify multiple sorted sets.
The command will act on the first non-empty set encountered:

```shell
dragonfly$> ZADD zset1 1 "a" 2 "b"
(integer) 2

dragonfly$> ZADD zset2 1 "x" 3 "y"
(integer) 2

dragonfly$> BZPOPMAX zset1 zset2 0
1) "zset1"  # Even though 'zset2' has a higher score, 'zset1' is popped first because it was specified first.
2) "b"
3) "2"
```

### Indefinite Blocking

By setting the `timeout` value to `0`, the connection will block indefinitely until a new element can be popped:

```shell
dragonfly$> BZPOPMAX somezset 0
# The connection will block until a new element is added to 'somezset'.
```

## Best Practices

- Use `BZPOPMAX` for priority job queues, where tasks with higher scores (priority) must be processed first.
- Set a reasonable timeout to avoid blocking connections permanently unless you specifically need indefinite blocking.

## Common Mistakes

- It can be easy to confuse the `timeout` parameter with `key` names if you're not careful with the syntax.
- Using the command without setting an appropriate `timeout`, such as setting it too high when the operation can affect client responsiveness.
- Confusing the key with the element of the sorted set in response.
  `BZPOPMAX` returns the key from which the member was popped as well, not just the member itself.

## FAQs

### What happens if the timeout is set to zero?

If the timeout is set to `0`, the connection will block indefinitely until a new element can be popped from the sorted set(s).

### Can I block on multiple sorted sets?

Yes, `BZPOPMAX` accepts multiple sorted set keys and will pop from the first non-empty sorted set, going through the list of keys from left to right, in the order they are provided.

### What happens if all keys are empty?

If all the provided sorted sets are empty or don't exist, `BZPOPMAX` returns `nil` after the timeout elapses.

### Does the command work with negative timeouts?

No, the `timeout` parameter must be a non-negative integer or floating point value specifying the maximum time in seconds to wait for an element to pop.
