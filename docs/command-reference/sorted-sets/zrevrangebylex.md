---
description: Learn how to use Redis ZREVRANGEBYLEX command to return all members of a sorted set between a range of lexicographical order in reverse.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGEBYLEX

<PageTitle title="Redis ZREVRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZREVRANGEBYLEX` command in Redis is used to return a range of members in a sorted set, specified by a lexicographical range, in reverse order. This is particularly useful when you need to retrieve elements stored in a specific lexicographical order but starting from the highest to the lowest values.

## Syntax

```plaintext
ZREVRANGEBYLEX key max min [LIMIT offset count]
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **max**: The maximum value in the lexicographical range (inclusive or exclusive).
- **min**: The minimum value in the lexicographical range (inclusive or exclusive).
- **LIMIT offset count**: Optional argument to limit the number of elements returned with an offset.

Lexicographical range limits:

- To specify open intervals, use parentheses `(`.
- To specify closed intervals, use brackets `[`.
- Special values `+` and `-` can be used for positive and negative infinity, respectively.

## Return Values

Returns an array of elements in the specified reversed lexical range. If no elements are found, an empty array is returned.

## Code Examples

```cli
dragonfly> ZADD myzset 0 "apple" 0 "banana" 0 "cherry" 0 "date"
(integer) 4
dragonfly> ZREVRANGEBYLEX myzset [cherry [banana
1) "cherry"
2) "banana"
dragonfly> ZREVRANGEBYLEX myzset (cherry (banana
(empty array)
dragonfly> ZREVRANGEBYLEX myzset + -
1) "date"
2) "cherry"
3) "banana"
4) "apple"
dragonfly> ZREVRANGEBYLEX myzset [date [apple LIMIT 1 2
1) "cherry"
2) "banana"
```

## Best Practices

- Ensure that the sorted set is not too large when using the `LIMIT` option to avoid heavy memory usage.
- Be cautious with lexicographical ranges as they can be inclusive or exclusive, impacting the results.

## Common Mistakes

- Misunderstanding the inclusive `[]` and exclusive `()` syntax for specifying the range, which can lead to unexpected results.
- Forgetting to handle cases where the resultant set might be empty, especially in application logic.

## FAQs

### What happens if the `key` does not exist?

If the specified sorted set key does not exist, `ZREVRANGEBYLEX` returns an empty array.

### Can `ZREVRANGEBYLEX` work with numeric scores?

No, `ZREVRANGEBYLEX` operates purely on the lexicographical ordering of the elements, not their scores.
