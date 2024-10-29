---
description: Use Redis ZREMRANGEBYLEX to remove sorted set members within a lexicographical range, plus expert tips beyond official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYLEX

<PageTitle title="Redis ZREMRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREMRANGEBYLEX` command is used to remove members from a sorted set, specifically those members whose names (lexicographically) fall within a specified range.

This command is most useful when you want to perform lexicographical operations with sorted sets, such as cleaning up or culling string-based range data within the sorted set.

## Syntax

```shell
ZREMRANGEBYLEX key min max
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements removed by the operation.
- **ACL categories:** @write, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set to modify.
- `min`: The minimum lexicographical boundary (inclusive or exclusive) for member removal.
- `max`: The maximum lexicographical boundary (inclusive or exclusive) for member removal.

### Lexicographical Range Specification:

- By default, both `min` and `max` are inclusive.
- Use `(` to specify that the range is **exclusive**. For example, `(a` is exclusive of the member with value `a`.
- `-` represents the smallest possible member (i.e., less than any valid string).
- `+` represents the largest possible member (i.e., greater than any valid string).

## Return Values

The command returns an integer indicating the number of members removed from the sorted set.

## Code Examples

### Basic Example

Remove members between "alpha" and "delta" inclusively:

```shell
dragonfly> ZADD myzset 0 alpha 0 bravo 0 charlie 0 delta 0 echo
(integer) 5
dragonfly> ZREMRANGEBYLEX myzset [alpha] [delta]
(integer) 4
dragonfly> ZRANGE myzset 0 -1
1) "echo"
```

### Exclusive Range Removal

Remove an inclusive-to-exclusive range, excluding "bravo":

```shell
dragonfly> ZADD myzset 0 alpha 0 bravo 0 charlie 0 delta 0 echo
(integer) 5
dragonfly> ZREMRANGEBYLEX myzset [alpha] (charlie
(integer) 2
dragonfly> ZRANGE myzset 0 -1
1) "charlie"
2) "delta"
3) "echo"
```

### Removing All Members in a Lexicographical Range

Remove everything up to "delta" inclusively:

```shell
dragonfly> ZADD myzset 0 alpha 0 bravo 0 charlie 0 delta 0 echo
(integer) 5
dragonfly> ZREMRANGEBYLEX myzset - [delta]
(integer) 4
dragonfly> ZRANGE myzset 0 -1
1) "echo"
```

### Completely Clearing a Set With a Large Lexicographical Range

Use `ZREMRANGEBYLEX` to remove all members of a sorted set easily:

```shell
dragonfly> ZADD myzset 0 alpha 0 bravo 0 charlie 0 delta 0 echo
(integer) 5
dragonfly> ZREMRANGEBYLEX myzset - +
(integer) 5
dragonfly> ZRANGE myzset 0 -1
(empty array)
```

## Best Practices

- For optimal performance, ensure your use case logically fits lexicographical ordering.
  `ZREMRANGEBYLEX` works best when you're filtering or trimming sets based on string ranges.
- If you're unsure about the lexicographical boundaries, use combinations of `"[", "("`, and the inclusive/exclusive markers to adjust the range.
- To clear specific portions of a set, particularly members that belong lexicographically to name clusters, use a smart combination of `ZREMRANGEBYLEX` with inclusive/exclusive ranges to target and remove only desired members.

## Common Mistakes

- Confusing inclusive and exclusive boundaries: Make sure you're clear whether you're including or excluding specific values when using `"("` and `"[ "` to define the range.
- Using `ZREMRANGEBYLEX` on non-sorted set types will result in an error.
- Misunderstanding that lexicographical order operates on a binary level and that it may behave differently compared to alphabetical or natural sorting.

## FAQs

### What happens if the `key` does not exist?

If the key does not exist, `ZREMRANGEBYLEX` will return `0` as no members exist to be removed.

### Can I use lexicographical ranges that extend beyond existing elements?

Yes, you can specify broad ranges using `-` and `+` as lexicographical boundaries. If the range extends beyond the existing minimum or maximum members, no error occurs.
The command will simply remove all elements within the included range based on existing members.
