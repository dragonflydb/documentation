---
description: Learn how to use Redis ZREVRANGEBYLEX command to return all members of a sorted set between a range of lexicographical order in reverse.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGEBYLEX

<PageTitle title="Redis ZREVRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZREVRANGEBYLEX` command is used to return a range of members in a sorted set, where the elements are lexicographically ordered within a specific range, but in reverse order (from higher to lower strings).
This is particularly useful for retrieving ordered elements when the lexicographical order of string values matters, often in cases like word dictionaries, leaderboard systems, or alphabetical searches.

## Syntax

```shell
ZREVRANGEBYLEX key max min [LIMIT offset count]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set.
- `max`: The maximum element (inclusive or exclusive depending on usage) in the lexicographical range.
- `min`: The minimum element (inclusive or exclusive depending on usage) in the lexicographical range.
- `LIMIT offset count` (optional): Limits the number of elements returned. `offset` specifies how many elements to skip, and `count` specifies the maximum number of elements to return.

## Return Values

The command returns an array of strings representing the elements in reverse lexicographical order between `max` and `min`.

## Code Examples

### Basic Example

Return elements in reverse lexicographical order between `"d"` and `"b"` (inclusive):

```shell
dragonfly> ZADD myzset 0 "a" 0 "b" 0 "c" 0 "d" 0 "e"
(integer) 5
dragonfly> ZREVRANGEBYLEX myzset "[d" "[b"
1) "d"
2) "c"
3) "b"
```

### Exclusive Range Example

Return elements between `"d"` (exclusive) and `"b"` (inclusive):

```shell
dragonfly> ZADD myzset 0 "a" 0 "b" 0 "c" 0 "d" 0 "e"
(integer) 5
dragonfly> ZREVRANGEBYLEX myzset "(d" "[b"
1) "c"
2) "b"
```

### Using `LIMIT` to Restrict Output

Return only the first 2 elements in reverse lexicographical order between `"z"` and `"a"`, skipping the first element (`offset=1`):

```shell
dragonfly> ZADD myzset 0 "a" 0 "b" 0 "c" 0 "d" 0 "e" 0 "f"
(integer) 6
dragonfly> ZREVRANGEBYLEX myzset "[f" "[a" LIMIT 1 2
1) "e"
2) "d"
```

## Best Practices

- When dealing with large sorted sets, you should apply the `LIMIT` option to control the number of elements returned.
  This improves performance and helps avoid overwhelming system memory.
- Ensure that the provided `min` and `max` are valid lexicographical ranges (i.e., string values), and consider whether you want the range to include or exclude the boundary elements using parentheses `()` (exclusive) and brackets `[]` (inclusive).

## Common Mistakes

- Using the wrong order of `max` and `min`: `ZREVRANGEBYLEX` expects `max` to be greater than `min` in lexicographical order, as the range starts from higher to lower.
- Ignoring the difference between inclusive and exclusive syntax when specifying the `max` and `min` parameters. `[]` includes the boundary, while `()` excludes it.

## FAQs

### What happens if the key does not exist?

If the specified key does not exist, `ZREVRANGEBYLEX` returns an empty array.

### Can I use the command with non-string elements in the set?

No, the command works only with string members, as it operates based on lexicographical (alphabetical) ordering, which does not apply to numeric values.

### What happens if no elements in the range satisfy the criteria?

If no members in the sorted set fall within the specified range, an empty array is returned.
