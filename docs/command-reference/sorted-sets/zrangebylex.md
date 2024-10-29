---
description: Learn to use the Redis ZRANGEBYLEX command to retrieve elements by their lexical range in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGEBYLEX

<PageTitle title="Redis ZRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANGEBYLEX` command is used to return a range of members in a sorted set, filtered by the member's lexicographical order.
It is especially useful for situations where you need to retrieve elements based purely on their defined string order, rather than by their scores.
This command offers a convenient way to perform efficient range queries on the lexicographical ordering of the elements in a sorted set.

## Syntax

```shell
ZRANGEBYLEX key min max [LIMIT offset count]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set where the range query is performed.
- `min`: The minimum lexicographical value (inclusive or exclusive). Use `(` to exclude the value and `[` to include it.
- `max`: The maximum lexicographical value (inclusive or exclusive). Again, use `[` to include the value and `(` to exclude it.
- `LIMIT offset count` (optional): Allows you to limit the number of elements returned starting from a specific position (`offset`), and up to the maximum number of elements (`count`) to return.

## Return Values

A list of members in the sorted set that fall within the specified lexicographical range.

## Code Examples

### Basic Example: Retrieve Members in a Lexicographical Range

Let's create a sorted set of words and retrieve words that fall between `apple` and `banana` inclusively:

```shell
dragonfly> ZADD fruits 0 apple 0 apricot 0 avocado 0 banana 0 berry
(integer) 5
dragonfly> ZRANGEBYLEX fruits [apple [banana
1) "apple"
2) "apricot"
3) "avocado"
4) "banana"
```

### Exclusive Range

You can exclude the start or end of the range by using parentheses `(` instead of square brackets `[`:

```shell
dragonfly> ZRANGEBYLEX fruits (apple [banana
1) "apricot"
2) "avocado"
3) "banana"
```

### Using `LIMIT` to Restrict Results

You can limit the number of results by specifying an `offset` and `count`:

```shell
dragonfly> ZRANGEBYLEX fruits [a [z LIMIT 1 2
1) "apricot"
2) "avocado"
```

In this example, the query starts from the second lexicographically-smallest member (`offset` = 1) and returns up to 2 members (`count` = 2).

### Querying a Range with No Matching Elements

If no elements fall within the specified range, the command will return an empty list:

```shell
dragonfly> ZRANGEBYLEX fruits [zzz [zzzz
(empty array)
```

## Best Practices

- Take advantage of `[` or `(` when defining lexicographical bounds to specify whether to include or exclude the boundary values.
- Use the `LIMIT` clause to avoid processing too many elements when you only need a subset of the range.
- Use `ZRANGEBYLEX` on datasets where elements are naturally ordered lexicographically, such as dictionary words or sequential, lexicographically sortable IDs.

## Common Mistakes

- Forgetting to use the correct boundary markers (`[` for inclusive, `(` for exclusive) in `min` and `max` parameters.
- Failing to specify the lexicographical ordering when intending to use string-based ordering and mistakenly using `ZSCORE` operations instead.
- Misunderstanding that `ZRANGEBYLEX` operates only on elements themselves, and not on their scores.

## FAQs

### Can `ZRANGEBYLEX` work with numeric scores?

No, `ZRANGEBYLEX` operates strictly on the lexicographical ordering of the members in a sorted set, regardless of their scores.
To perform range queries on numeric scores, use `ZRANGEBYSCORE`.

### What happens if the key does not exist?

If the key does not exist, `ZRANGEBYLEX` returns an empty array because there are no members in the sorted set.

### Can I use `ZRANGEBYLEX` with a set that has numeric-like string values?

Yes, you can use numeric-like strings such as `"123"`, `"456"`, etc.
`ZRANGEBYLEX` will still interpret these strings lexicographically, meaning `"123"` may come before `"12"` because it's based on string comparison, not numeric order.
