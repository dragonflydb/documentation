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
- `min` and `max`:
  - The minimum and maximum lexicographical values to filter the members.
  - Valid `start` and `stop` values must start with `(` or `[` to indicate exclusive or inclusive bounds respectively.
  - The `+` and `-` special values can be used to specify positive and negative infinity strings, respectively.

## Return Values

- The command returns an integer indicating the number of members removed from the sorted set.

## Code Examples

### Basic Example

Remove members between `alpha` and `delta` inclusively:

```shell
dragonfly$> ZADD myzset 0 "alpha" 0 "bravo" 0 "charlie" 0 "delta" 0 "echo"
(integer) 5

dragonfly$> ZREMRANGEBYLEX myzset [alpha [delta
(integer) 4

dragonfly$> ZRANGE myzset 0 -1
1) "echo"
```

### Exclusive Range Removal

Remove an inclusive-to-exclusive range, excluding `alpha` but including `delta`:

```shell
dragonfly$> ZADD myzset 0 "alpha" 0 "bravo" 0 "charlie" 0 "delta" 0 "echo"
(integer) 5

dragonfly$> ZREMRANGEBYLEX myzset (alpha [delta
(integer) 3

dragonfly$> ZRANGE myzset 0 -1
1) "alpha"
2) "echo"
```

### Removing All Members in a Lexicographical Range

Remove everything up to `delta` inclusively:

```shell
dragonfly$> ZADD myzset 0 "alpha" 0 "bravo" 0 "charlie" 0 "delta" 0 "echo"
(integer) 5

dragonfly$> ZREMRANGEBYLEX myzset - [delta
(integer) 4

dragonfly$> ZRANGE myzset 0 -1
1) "echo"
```

### Completely Clearing a Set With a Large Lexicographical Range

Use `ZREMRANGEBYLEX` and the `-` and `+` special values to remove all members in a sorted set:

```shell
dragonfly$> ZADD myzset 0 alpha 0 bravo 0 charlie 0 delta 0 echo
(integer) 5

dragonfly$> ZREMRANGEBYLEX myzset - +
(integer) 5

dragonfly$> ZRANGE myzset 0 -1
(empty array)
```

## Best Practices

- For optimal performance, ensure your use case logically fits lexicographical ordering.
  `ZREMRANGEBYLEX` works best when you're filtering or trimming sets based on string ranges.
- If you're unsure about the lexicographical boundaries, use combinations of `[` and `(` as the inclusive/exclusive markers to adjust the range.

## Common Mistakes

- Confusing inclusive and exclusive boundaries: Make sure you're clear whether you're including or excluding specific values when using `[` and `(` to define the range.
- Using `ZREMRANGEBYLEX` on non-sorted set types will result in an error.

## FAQs

### What happens if the `key` does not exist?

If the key does not exist, `ZREMRANGEBYLEX` will return `0` as no members exist to be removed.

### Can I use lexicographical ranges that extend beyond existing elements?

Yes, you can specify broad ranges using `-` and `+` as lexicographical boundaries. If the range extends beyond the existing minimum or maximum members, no error occurs.
The command will simply remove all elements within the included range based on existing members.
