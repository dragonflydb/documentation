---
description: Learn to use the Redis ZRANGEBYLEX command to retrieve elements by their lexical range in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGEBYLEX

<PageTitle title="Redis ZRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZRANGEBYLEX` command in Redis is used to return a range of members in a sorted set, where the elements are ordered lexicographically (alphabetically) by their value. This command is particularly useful for operations that need to fetch members from a sorted set within a specific lexicographical range, such as autocomplete suggestions or alphabetical filtering.

## Syntax

```
ZRANGEBYLEX key min max [LIMIT offset count]
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **min**: The minimum value in the lexicographical range to include. Use `-` to represent the lowest possible string value.
- **max**: The maximum value in the lexicographical range to include. Use `+` to represent the highest possible string value.
- **LIMIT offset count** _(optional)_: Limits the number of elements returned. `offset` specifies the number of elements to skip and `count` sets the maximum number of elements to return.

## Return Values

Returns an array of elements in the specified range.

### Examples:

- If there are matching elements: `["alpha", "beta", "gamma"]`
- If no elements match: `[]`

## Code Examples

```cli
dragonfly> ZADD myzset 0 "alpha"
(integer) 1
dragonfly> ZADD myzset 0 "beta"
(integer) 1
dragonfly> ZADD myzset 0 "gamma"
(integer) 1
dragonfly> ZADD myzset 0 "delta"
(integer) 1
dragonfly> ZRANGEBYLEX myzset "[a" "[g"
1) "alpha"
2) "beta"
3) "delta"

dragonfly> ZRANGEBYLEX myzset "[a" "[d" LIMIT 1 2
1) "beta"
2) "delta"
```

## Best Practices

- Ensure your elements are unique if they have the same score since `ZRANGEBYLEX` orders elements lexicographically when scores are equal.
- Utilize the `LIMIT` option to paginate through large sets efficiently.

## Common Mistakes

- Confusing lexicographical order with numerical order. `ZRANGEBYLEX` does not sort by numerical value but by string comparison.
- Using incorrect syntax for `min` and `max`. Always include square brackets (`[ ]`) to indicate inclusive ranges.

## FAQs

### What happens if I use `(` instead of `[` in `min` or `max`?

Using `(` indicates an exclusive range. For example, `ZRANGEBYLEX myzset "(alpha" "[gamma"` will exclude `alpha` from the results.

### Can I use `ZRANGEBYLEX` on non-string elements?

No, `ZRANGEBYLEX` operates on string comparisons, so it isn't suitable for non-string elements.
