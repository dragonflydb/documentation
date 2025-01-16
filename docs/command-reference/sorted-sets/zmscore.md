---
description: Learn to use the Redis ZMSCORE command to return scores for given members in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZMSCORE

<PageTitle title="Redis ZMSCORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZMSCORE` command is used to retrieve the scores associated with the given members in a sorted set stored at a specified key.
It is useful when you need to quickly fetch the ranking or priority values of multiple elements from a given sorted set.

## Syntax

```shell
ZMSCORE key member [member ...]
```

- **Time complexity:** O(N) where N is the number of members being requested.
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key name of the sorted set stored in the database.
- `member`: One or more members for which the associated score is requested.

## Return Values

The command returns an array of scores corresponding to the list of `member` inputs.
If a member is not part of the sorted set, `nil` is returned for that specific member.

## Code Examples

### Basic Example

Retrieve scores for multiple members in a sorted set:

```shell
dragonfly$> ZADD myzset 1 "Alice" 2 "Bob" 3 "Charlie"
(integer) 3

dragonfly$> ZMSCORE myzset "Alice" "Charlie"
1) "1"
2) "3"
```

### Example with Mixed Member Existence

Query the sorted set for both existing and non-existing members:

```shell
dragonfly$> ZADD myzset 1 "Alice" 2 "Bob" 3 "Charlie"
(integer) 3

dragonfly$> ZMSCORE myzset "Alice" "Bob" "Unknown"
1) "1"
2) "2"
3) (nil)
```

`"Alice"` and `"Bob"` are found with their respective scores, but "Unknown" does not exist.

## Best Practices

- Use `ZMSCORE` when you need to retrieve multiple scores in a single command to save round-trip time to the server.
- Make sure no duplicate members are included in your input to avoid redundant evaluations.
- If the set contains many elements, ensure that the queried members are part of the current application logic to avoid unnecessary `nil` values.

## Common Mistakes

- Requesting members not part of the sorted set and assuming the command will give `0`—instead, it returns `nil`.
- Forgetting that `ZMSCORE` returns string representations of the scores, not integers or floats.

## FAQs

### What happens if the key does not exist?

If the key does not exist, the command returns nil for each member.

### How does `ZMSCORE` handle multiple members?

It returns an array where each element corresponds to the score of a requested `member`. Non-existing members return `nil` in the respective position within the array.
