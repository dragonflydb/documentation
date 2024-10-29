---
description: Learn how to use the Redis BZPOPMAX command to remove and return the highest score member from sorted sets, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# BZPOPMAX

<PageTitle title="Redis BZPOPMAX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BZPOPMAX` command is used to remove and return the member with the highest score in a sorted set.
If the sorted set is empty, the command will block the connection for a specified timeout until a member is available to pop.
This makes it particularly useful for creating delayed or sorted workflows such as job queues where items with the highest priority need to be processed first.

## Syntax

```shell
BZPOPMAX key [key ...] timeout
```

- **Time complexity:** O(log(N)) with N being the number of elements in the sorted set.
- **ACL categories:** @write, @sortedset, @fast, @blocking

## Parameter Explanations

- `key`: One or more keys, each representing a sorted set.
- `timeout`: The maximum number of seconds to wait if all the provided sorted sets are empty. A `0` timeout means no block, and negative timeouts will cause indefinite blocking.

## Return Values

The command returns a three-element array containing:

- The name of the sorted set that the element was popped from.
- The highest score element.
- The score itself.

If the timeout expires without any elements to pop, `nil` is returned.

## Code Examples

### Basic Example

Pop the highest score element from a sorted set:

```shell
dragonfly> ZADD myzset 1 "item1" 2 "item2" 3 "item3"
(integer) 3
dragonfly> BZPOPMAX myzset 0
1) "myzset"
2) "item3"
3) "3"
```

### Blocking for Elements

If the sorted set is empty, `BZPOPMAX` will wait for new elements or until the timeout:

```shell
dragonfly> ZADD myzset 1 "item1" 2 "item2"
(integer) 2
dragonfly> ZPOPMAX myzset
1) "item2"
2) "2"
dragonfly> ZPOPMAX myzset
1) "item1"
2) "1"
dragonfly> BZPOPMAX myzset 5
(nil)  # No elements in the sorted set, waited for 5 seconds and then returned nil.
```

### Using Multiple Keys

You can specify multiple sorted sets.
The command will act on the first non-empty set encountered:

```shell
dragonfly> ZADD zset1 1 "a" 2 "b"
(integer) 2
dragonfly> ZADD zset2 1 "x" 3 "y"
(integer) 2
dragonfly> BZPOPMAX zset1 zset2 0
1) "zset2"
2) "y"
3) "3"
```

### Indefinite Blocking

By setting the `timeout` value to a negative number, the connection will block indefinitely until a new element can be popped:

```shell
dragonfly> BZPOPMAX somezset -1
# The connection will block until a new element is added to 'somezset'.
```

## Best Practices

- Use `BZPOPMAX` for priority job queues, where tasks with higher scores (priority) must be processed first.
- Set a reasonable timeout to avoid blocking connections permanently unless you specifically need indefinite blocking.

## Common Mistakes

- Using `BZPOPMAX` on non-sorted set types can result in an error. Ensure that you only use this command on sorted sets.
- Assuming this command will pop values from other types like lists; use other blocking list commands such as `BLPOP` or `BRPOP` in those cases.
- It's easy to confuse the timeout parameter with key names if you're not careful with the syntax.

## FAQs

### What happens if the timeout is set to zero?

If the timeout is set to `0`, the command will not block. Instead, it will return immediately with either a popped element or `nil` if the sorted sets are empty.

### Can I block on multiple sorted sets?

Yes, `BZPOPMAX` accepts multiple sorted set keys and will pop from the first non-empty sorted set, going through the list of keys from left to right.

### What is the typical use case for `BZPOPMAX`?

`BZPOPMAX` is often used in priority queues, where jobs with higher priority (indicated by score) need to be processed as soon as they are available. If no jobs exist, the command waits for new ones.
