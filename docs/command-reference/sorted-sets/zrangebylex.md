---
description: Learn to use the Redis ZRANGEBYLEX command to retrieve elements by their lexical range in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGEBYLEX

<PageTitle title="Redis ZRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANGEBYLEX` command is used to return a range of members in a sorted set, filtered by the member's lexicographical order.
It is especially useful for situations where you need to **retrieve elements with the same score based on their defined string order**.
This command offers a convenient way to perform efficient range queries on the lexicographical ordering of the elements in a sorted set.
Note that if the elements in the sorted set have different scores, the returned elements are unspecified.

## Syntax

```shell
ZRANGEBYLEX key min max [LIMIT offset count]
```

- **Time complexity:** O(log(N)+M) with N being the number of elements in the sorted set and M the number of elements being returned. If M is constant (e.g. always asking for the first 10 elements with LIMIT), you can consider it O(log(N)).
- **ACL categories:** @read, @sortedset, @slow

## Parameter Explanations

- `key`: The key of the sorted set where the range query is performed.
- `min` and `max`:
  - The minimum and maximum lexicographical values to filter the members.
  - Valid `min` and `max` values must start with `(` or `[` to indicate exclusive or inclusive bounds respectively.
  - The `+` and `-` special values can be used to specify positive and negative infinity strings, respectively.
- `LIMIT offset count` (optional): If specified, the command returns a subset of the elements within the specified range.
  - `offset`: The starting index of the subset (zero-based).
  - `count`: The number of elements to return. A negative `count` returns all elements from the `offset`.

## Return Values

- A list of members in the sorted set that fall within the specified lexicographical range.

## Code Examples

### Basic Example: Retrieve Members in a Lexicographical Range

Let's create a sorted set of words and retrieve words that fall between `apple` and `banana` inclusively:

```shell
dragonfly$> ZADD fruits 0 apple 0 apricot 0 avocado 0 banana 0 berry
(integer) 5

dragonfly$> ZRANGEBYLEX fruits [apple [banana
1) "apple"
2) "apricot"
3) "avocado"
4) "banana"
```

### Exclusive Range

You can exclude the start or end of the range by using parentheses `(` instead of square brackets `[`:

```shell
dragonfly$> ZADD fruits 0 apple 0 apricot 0 avocado 0 banana 0 berry
(integer) 5

dragonfly$> ZRANGEBYLEX fruits (apple [banana
1) "apricot"
2) "avocado"
3) "banana"
```

### Using `LIMIT` to Restrict Results

You can limit the number of results by specifying an `offset` and `count`:

```shell
dragonfly$> ZADD fruits 0 apple 0 apricot 0 avocado 0 banana 0 berry
(integer) 5

dragonfly$> ZRANGEBYLEX fruits [a [z LIMIT 1 2
1) "apricot"
2) "avocado"
```

In this example, the query starts from the second-smallest member (`offset=1`) and returns up to 2 members (`count=2`).

### A Range with No Matching Elements

If no elements fall within the specified lexicographical range, the command will return an empty list:

```shell
dragonfly$> ZADD fruits 0 apple 0 apricot 0 avocado 0 banana 0 berry
(integer) 5

# No elements between "zzz" and "zzzz".
dragonfly$> ZRANGEBYLEX fruits [zzz [zzzz
(empty array)

# No elements between "zzz" and the positive infinite string.
dragonfly$> ZRANGEBYLEX fruits [zzz +
(empty array)
```

### Elements with Different Scores

When elements have different scores, the returned elements are unspecified:

```shell
# Here, the 'apple' element has a score of 1.
dragonfly$> ZADD fruits 1 apple 0 apricot 0 avocado 0 banana 0 berry
(integer) 5

# We cannot rely on the order of elements with different scores while using ZRANGEBYLEX.
dragonfly$> ZRANGEBYLEX fruits - +
1) "apricot"
2) "avocado"
3) "banana"
4) "berry"
5) "apple"
```

## Best Practices

- Take advantage of `[` or `(` when defining lexicographical bounds to specify whether to be inclusive or exclusive.
- Use the `LIMIT` clause to avoid processing too many elements when you only need a subset of the range.
- Use `ZRANGEBYLEX` on datasets where elements are naturally ordered lexicographically, such as dictionary words or sequential, lexicographically sortable IDs.

## Common Mistakes

- Forgetting that `ZRANGEBYLEX` operates on lexicographical ordering, not numeric scores.
- Forgetting to use the correct boundary markers (`[` for inclusive, `(` for exclusive) in `min` and `max` parameters.
- Using invalid ranges (`min` > `max`) will always return an empty array.
- Misunderstanding that the `LIMIT` clause is applied after filtering, meaning it limits how many results are returned but does not affect the lexicographical range.

## FAQs

### Can I use `ZRANGEBYLEX` with a set that has numeric-like string values?

Yes, you can use numeric-like strings such as `"123"`, `"456"`, etc. as members in a sorted set.
However, `ZRANGEBYLEX` will still interpret these strings lexicographically.

### What happens if the key does not exist?

If the key does not exist, `ZRANGEBYLEX` returns an empty array because there are no members in the sorted set.
