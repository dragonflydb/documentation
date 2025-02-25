---
description: Learn to use the Redis ZDIFFSTORE to calculate and store the difference of sorted sets.
---

import PageTitle from '@site/src/components/PageTitle';

# ZDIFFSTORE

<PageTitle title="Redis ZDIFFSTORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZDIFFSTORE` command is used to compute the difference between the members of multiple sorted sets and store it at the destination set.
This command is useful when you need to identify elements that belong to one sorted set, but not to others, and is helpful in scenarios like finding unique elements or filtering out overlap between sets.

## Syntax

```shell
ZDIFFSTORE destination numkeys key [key ...]
```

- **Time complexity:** O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `destination`: Where the computed difference is stored.
- `numkeys`: The number of input sorted sets.
- `key`: The keys of the sorted sets to compare.

## Return Values

- The number of members in the resulting sorted set at destination.

## Code Examples

### Basic Example: Finding Differences Between Two Sets

Return the members found in the first sorted set but not in the second:

```shell
dragonfly$> ZADD myzset1 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly$> ZADD myzset2 2 "two" 4 "four"
(integer) 2

dragonfly$> ZDIFFSTORE result 2 myzset1 myzset2
(integer) 2

dragonfly$> ZRANGE result 0 -1
1) "one"
2) "three"
```

## Best Practices

- Use `ZDIFFSTORE` when you need to isolate unique elements in one sorted set compared to others.
- Always ensure that the correct number of `numkeys` is provided to avoid errors or unwanted results.

## Common Mistakes

- Forgetting to specify the correct number of sorted sets in `numkeys`.
  The first argument should match the number of subsequent sorted set keys passed to the command.

## FAQs

### What happens if a key does not exist?

If one or more of the keys do not exist, they are treated as empty sets, and the difference is calculated accordingly.

### What happens if I provide just one key?

If only one key is provided in the `ZDIFFSTORE` command, it will simply store that set in `destination`,
as there are no additional sets to subtract from it.

### What happens if `destination` already exists?

If the `destination` key already exists, it will be overwritten.
