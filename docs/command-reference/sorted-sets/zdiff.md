---
description: Learn to use the Redis ZDIFF command to compute the difference of sorted sets.
---

import PageTitle from '@site/src/components/PageTitle';

# ZDIFF

<PageTitle title="Redis ZDIFF Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZDIFF` command is used to compute the difference between the members of multiple sorted sets.
This command is useful when you need to identify elements that belong to one sorted set, but not to others, and is helpful in scenarios like finding unique elements or filtering out overlap between sets.

## Syntax

```shell
ZDIFF numkeys key [key ...] [WITHSCORES]
```

- **Time complexity:** O(L + (N-K)log(N)) worst case where L is the total number of elements in all the sets, N is the size of the first set, and K is the size of the result set.
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `numkeys`: The number of input sorted sets.
- `key`: The keys of the sorted sets to compare.
- `WITHSCORES` (optional): If specified, the command returns both the members and their respective scores.

## Return Values

- Without `WITHSCORES`: The command returns an array of members that are in the first sorted set but not in any of the other given sorted sets.
- With `WITHSCORES`: The command returns an array where each member is followed by its score.

## Code Examples

### Basic Example: Finding Differences Between Two Sets

Return the members found in the first sorted set but not in the second:

```shell
dragonfly$> ZADD myzset1 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly$> ZADD myzset2 2 "two" 4 "four"
(integer) 2

dragonfly$> ZDIFF 2 myzset1 myzset2
1) "one"
2) "three"
```

In this example, `"one"` and `"three"` are present in `myzset1` but not present in `myzset2`.

### Example with `WITHSCORES`

Return both the members and their scores for the difference between two sets:

```shell
dragonfly$> ZADD myzset1 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly$> ZADD myzset2 2 "two" 4 "four"
(integer) 2

dragonfly$> ZDIFF 2 myzset1 myzset2 WITHSCORES
1) "one"
2) "1"
3) "three"
4) "3"
```

### Multiple Sets Difference Example

Find elements present in the first sorted set but missing in the other two sorted sets:

```shell
dragonfly$> ZADD myzset1 1 "one" 2 "two" 3 "three" 4 "four"
(integer) 4

dragonfly$> ZADD myzset2 3 "three" 4 "four"
(integer) 2

dragonfly$> ZADD myzset3 1 "one" 5 "five"
(integer) 2

dragonfly$> ZDIFF 3 myzset1 myzset2 myzset3
1) "two"
```

In this case, only `"two"` is present in `myzset1` but not in `myzset2` or `myzset3`.

## Best Practices

- Use `ZDIFF` when you need to isolate unique elements in one sorted set compared to others.
- Always ensure that the correct number of `numkeys` is provided to avoid errors or unwanted results.
- If you're working with large sets, consider the time complexity and whether you need `WITHSCORES`, as fetching scores increases the size of the returned data.

## Common Mistakes

- Forgetting to specify the correct number of sorted sets in `numkeys`. The first argument should match the number of subsequent sorted set keys passed to the command.
- Misunderstanding that `ZDIFF` only returns members and not their scores. Use `WITHSCORES` if the scores are required as part of the result.

## FAQs

### What happens if a key does not exist?

If one or more of the keys do not exist, they are treated as empty sets, and the difference is calculated accordingly.

### Can I use `ZDIFF` with sets that are not sorted sets?

No, `ZDIFF` only works with sorted sets. Passing keys of other types will result in an error.

### What happens if I provide just one key?

If only one key is provided in the `ZDIFF` command, it will simply return all the members of that sorted set, as there are no additional sets to subtract from it.
