---
description: Learn how to use the Redis ZLEXCOUNT command to count elements in a sorted set between two lexicographical values, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZLEXCOUNT

<PageTitle title="Redis ZLEXCOUNT Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZLEXCOUNT` command is used to count the number of elements in a sorted set that fall between a given lexicographical range (i.e., the dictionary order of the string values within the set).
It is useful in a wide range of scenarios, particularly when dealing with ordered or alphabetical sorting, range-based queries, or when managing complex datasets that require retrieval of elements within specific textual limits.

## Syntax

```shell
ZLEXCOUNT key min max
```

- **Time complexity:** O(log(N)) with N being the number of elements in the sorted set.
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key for the sorted set where the lexicographical counting occurs.
- `min`: The minimum lexicographical string value for the range query (inclusive or exclusive). Use `[` to include and `(` to exclude.
- `max`: The maximum lexicographical string value for the range query (inclusive or exclusive). Use `[` to include and `(` to exclude.

## Return Values

The command returns an integer indicating the number of members in the sorted set within the provided lexicographical range.

## Code Examples

### Basic Example

Count the number of elements in a lexicographical range in a sorted set:

```shell
dragonfly$> ZADD myset 0 a 0 b 0 c 0 d 0 e
(integer) 5
dragonfly$> ZLEXCOUNT myset [b [d
(integer) 3
```

In this example, the elements `b`, `c`, and `d` fall within the lexicographical range `[b, d]`, returning a count of `(3)`.

### Range with Exclusive Boundaries

Specify an exclusive upper range limit in a lexicographical query:

```shell
dragonfly$> ZADD myset 0 a 0 b 0 c 0 d 0 e
(integer) 5
dragonfly$> ZLEXCOUNT myset [b (d
(integer) 2
```

Here, only `b` and `c` fall within the range `[b, d)`, as `d` is excluded due to the `(`.

### Counting All Elements with a Lexicographical Range Across All Members

To count all elements in the sorted set, use `-` and `+` as argument values denoting the lowest and highest possible strings:

```shell
dragonfly$> ZADD myset 0 a 0 b 0 c 0 d 0 e
(integer) 5
dragonfly$> ZLEXCOUNT myset - +
(integer) 5
```

In this case, all members from `a` to `e` are counted.

### Limiting the Range to a Single Character

You can also query for a very specific range by using single-character bounds:

```shell
dragonfly$> ZADD myset 0 a 0 b 0 c 0 d 0 e
(integer) 5
dragonfly$> ZLEXCOUNT myset [c [c
(integer) 1
```

This example counts only the element `c`, as the range is constrained to `[c, c]`.

## Best Practices

- When using large sorted sets, lexicographical queries can be quite efficient for text-based range retrievals.
- Use inclusive and exclusive boundaries carefully (`[` and `(`) to define the exact range of elements you need.
- For lexicographical queries covering large segments with efficient performance, consider using `ZLEXCOUNT` instead of scanning large parts of the sorted set.

## Common Mistakes

- Assuming `ZLEXCOUNT` operates on numeric values—this command only works on lexicographical (text) comparisons.
- Misunderstanding the boundary markers `[`, `(`—inclusive and exclusive boundaries can lead to incorrect or unintended results if not used properly.
- Attempting to use the command on a key that does not map to a sorted set. This will result in an error.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZLEXCOUNT` will return `0`.

### Can I use `ZLEXCOUNT` with integer values?

While `ZLEXCOUNT` can technically handle integer-like strings, the values are still compared lexicographically, not numerically. This means `'100'` will come before `'20'` when sorted lexicographically.

### What does `-` and `+` mean in `ZLEXCOUNT` ranges?

When using `ZLEXCOUNT`, `-` represents the lowest possible string in lexicographical order, and `+` represents the highest.
This allows you to cover the entire range of possible elements in the sorted set.
