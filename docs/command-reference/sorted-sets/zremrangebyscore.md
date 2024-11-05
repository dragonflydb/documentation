---
description: Learn how to use Redis ZREMRANGEBYSCORE command to remove all members in a sorted set within the given scores.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYSCORE

<PageTitle title="Redis ZREMRANGEBYSCORE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZREMRANGEBYSCORE` command is used in Redis to remove all members in a sorted set that have a score within a specified range. Typical use cases include cleaning up expired data, implementing leaderboards where only scores within a certain range are relevant, or managing time-based series data.

## Syntax

```
ZREMRANGEBYSCORE key min max
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **min**: The minimum score (inclusive) of the range. This can be a number or one of the special values `-inf` (negative infinity) to represent the lowest possible score.
- **max**: The maximum score (inclusive) of the range. This can be a number or one of the special values `+inf` (positive infinity) to represent the highest possible score.

Special modifiers for `min` and `max`:

- Use `(` before a number to make the range exclusive. For example, `(1` means greater than 1 but not equal to 1.

## Return Values

The command returns the number of elements removed from the sorted set.

### Example Output

```cli
(integer) 3
```

## Code Examples

Remove members with scores between 1 and 2 (inclusive):

```cli
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly$> ZREMRANGEBYSCORE myzset 1 2
(integer) 2
dragonfly$> ZRANGE myzset 0 -1 WITHSCORES
1) "three"
2) "3"
```

Remove members with scores greater than 1 but less than 3:

```cli
dragonfly$> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly$> ZREMRANGEBYSCORE myzset (1 (3
(integer) 1
dragonfly$> ZRANGE myzset 0 -1 WITHSCORES
1) "one"
2) "1"
3) "three"
4) "3"
```

## Best Practices

- When working with large data sets, ensure your `min` and `max` ranges are correctly defined to avoid unintentional removal of important data.
- Consider using `ZRANGEBYSCORE` to preview the elements that will be deleted before executing `ZREMRANGEBYSCORE`.

## Common Mistakes

- Confusing inclusive and exclusive boundaries. Always double-check whether you intend to include or exclude the boundary values using parentheses.
- Not specifying the correct range, which might lead to either no deletions or deletion of more elements than intended.

## FAQs

**Q: Can I use floating-point numbers for the score range?**

A: Yes, `ZREMRANGEBYSCORE` supports floating-point numbers for both `min` and `max`.

**Q: What happens if the specified range does not match any elements?**

A: If no elements fall within the specified range, the return value will be `(integer) 0`, indicating no elements were removed.
