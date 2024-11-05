---
description: Learn to use the Redis ZCARD command to get the total number of elements in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZCARD

<PageTitle title="Redis ZCARD Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZCARD` command is used to return the number of members in a sorted set stored at a given key.
This is particularly useful when you need to monitor the size of a sorted set or implement pagination, leaderboards, or other order-based storage solutions.

## Syntax

```shell
ZCARD key
```

- **Time complexity:** O(1)
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set whose cardinality (number of members) is to be fetched.

## Return Values

The command returns an integer representing the number of members in the sorted set.
If the key does not exist or is not a sorted set, `0` is returned.

## Code Examples

### Basic Example

To get the number of members in a sorted set:

```shell
dragonfly$> ZADD myzset 1 "member1" 2 "member2" 3 "member3"
(integer) 3
dragonfly$> ZCARD myzset
(integer) 3
```

### When the Sorted Set is Empty

If the sorted set is empty or non-existent, the `ZCARD` command returns `0`.

```shell
dragonfly$> ZCARD emptyset
(integer) 0
```

### Using `ZCARD` for Pagination

Suppose you are building a leaderboard and need to know how many total players are ranked to help with pagination:

```shell
dragonfly$> ZADD leaderboard 100 "player1" 150 "player2" 200 "player3"
(integer) 3
dragonfly$> ZCARD leaderboard
(integer) 3
```

## Best Practices

- Since `ZCARD` only fetches the number of elements, it is safe to use even with large sets without performance concerns.
- Ideal for checking the size of sorted sets before executing more complex operations on large sets.

## Common Mistakes

- Assuming `ZCARD` can return detailed information about members; it only returns the count of elements.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZCARD` will return `0` since there are no members in a non-existent set.

### Can I use `ZCARD` on a non-sorted set?

No, `ZCARD` specifically works with sorted sets.
If you use it on a key that holds a different data type, Dragonfly will throw an error.
For counting members of a regular set, you should use the `SCARD` command.
