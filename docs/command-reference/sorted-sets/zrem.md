---
description: Learn how to use the Redis ZREM command to remove members from a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREM

<PageTitle title="Redis ZREM Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREM` command is used to remove one or more members from a sorted set stored at a specified key.
This can be useful when managing priority queues, leaderboards, or any scenario where members of a set need to be dynamically removed while maintaining ordering based on score.

## Syntax

```shell
ZREM key member [member ...]
```

- **Time complexity:** O(M\*log(N)) with N being the number of elements in the sorted set and M the number of elements to be removed.
- **ACL categories:** @write, @sortedset, @fast

## Parameter Explanations

- `key`: The sorted set from which members are to be removed.
- `member`: One or more members to remove from the sorted set. Members that do not exist are ignored.

## Return Values

The command returns an integer representing the number of members that were removed from the sorted set.

## Code Examples

### Basic Example

Remove a single member from a sorted set:

```shell
dragonfly> ZADD myzset 1 "alpha" 2 "beta" 3 "gamma"
(integer) 3
dragonfly> ZREM myzset "alpha"
(integer) 1
dragonfly> ZRANGE myzset 0 -1
1) "beta"
2) "gamma"
```

### Remove Multiple Members

You can also remove multiple members in one command:

```shell
dragonfly> ZADD myzset 1 "alpha" 2 "beta" 3 "gamma"
(integer) 3
dragonfly> ZREM myzset "alpha" "gamma"
(integer) 2
dragonfly> ZRANGE myzset 0 -1
1) "beta"
```

### Attempt to Remove Non-Existing Members

If you attempt to remove members that do not exist in the sorted set, they are simply ignored:

```shell
dragonfly> ZADD myzset 1 "alpha" 2 "beta"
(integer) 2
dragonfly> ZREM myzset "gamma" "delta"
(integer) 0  # No members were removed because "gamma" and "delta" don't exist.
```

## Best Practices

- Use `ZREM` in conjunction with other sorted set commands like `ZRANGE` and `ZADD` to maintain leaderboards, priority queues, or other ranked data structures.
- When removing members, consider batching multiple deletions in a single `ZREM` command to minimize round-trip time and improve performance.

## Common Mistakes

- Attempting to remove members from a key that is not a sorted set will result in an error.
- Expecting `ZREM` to return an error when attempting to remove non-existent members; instead, it simply returns the count of successfully removed members.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZREM` will return `0` since there are no members to remove.

### Can I use `ZREM` with an empty member list?

No, attempting to run `ZREM` without specifying at least one member will result in an error.
