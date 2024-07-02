---
description: Use Redis ZREMRANGEBYLEX to remove sorted set members within a lexicographical range, plus expert tips beyond official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYLEX

<PageTitle title="Redis ZREMRANGEBYLEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZREMRANGEBYLEX` command in Redis is used to remove all elements in a sorted set between a given lexicographical range. This command is useful when you need to efficiently manage subsets of strings in a sorted set, especially when the ordering is lexicographical.

## Syntax

```
ZREMRANGEBYLEX key min max
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **min**: The minimum lexicographical value (inclusive or exclusive). Use "[" for inclusive and "(" for exclusive.
- **max**: The maximum lexicographical value (inclusive or exclusive). Use "[" for inclusive and "(" for exclusive.

## Return Values

Returns the number of elements removed from the sorted set.

### Example Outputs

- `(integer) 2`: Indicates that two elements were removed.
- `(integer) 0`: Indicates no elements were removed.

## Code Examples

```cli
dragonfly> ZADD myzset 0 "apple"
(integer) 1
dragonfly> ZADD myzset 0 "banana"
(integer) 1
dragonfly> ZADD myzset 0 "cherry"
(integer) 1
dragonfly> ZREMRANGEBYLEX myzset "[banana" "[cherry"
(integer) 2
dragonfly> ZRANGE myzset 0 -1
1) "apple"
```

## Best Practices

- Ensure your lexicographical range bounds are correctly defined to avoid accidental data removal.
- Use this command when your use case specifically requires lexicographical ordering and removal. For numerical ranges, consider other commands like `ZREMRANGEBYSCORE`.

## Common Mistakes

- Confusing inclusive and exclusive bounds: `[banana` includes "banana", while `(banana` does not.
- Not specifying the correct bounds, which can lead to unexpected removals or no removals at all.

## FAQs

### What happens if I specify a non-existent range?

If the specified range doesn't match any elements in the sorted set, the command returns `(integer) 0`, indicating no elements were removed.

### Can I use ZREMRANGEBYLEX on non-string elements?

No, `ZREMRANGEBYLEX` is meant for sets with string elements. For numeric values, consider using commands like `ZREMRANGEBYSCORE`.
