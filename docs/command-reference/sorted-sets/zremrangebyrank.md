---
description: ⚡ Better than official Redis docs ⚡ Learn how to use Redis ZREMRANGEBYRANK command to remove all members in a sorted set within the given indexes.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREMRANGEBYRANK

<PageTitle title="Redis ZREMRANGEBYRANK Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

`ZREMRANGEBYRANK` removes all elements in a sorted set within the given rank range. This command is useful for trimming sets, removing outdated data, or maintaining a fixed number of records.

## Syntax

```plaintext
ZREMRANGEBYRANK key start stop
```

## Parameter Explanations

- `key`: The name of the sorted set.
- `start`: The starting rank (inclusive) to remove. Ranks are 0-based indices where 0 is the element with the smallest score.
- `stop`: The ending rank (inclusive) to remove.

## Return Values

The command returns an integer indicating the number of members removed.

### Examples:

- If three members are removed, it returns `(integer) 3`.
- If no members are found within the specified rank range, it returns `(integer) 0`.

## Code Examples

```cli
dragonfly> ZADD myset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZREMRANGEBYRANK myset 0 1
(integer) 2
dragonfly> ZRANGE myset 0 -1 WITHSCORES
1) "three"
2) "3"
```

## Best Practices

- Use `ZRANGEBYRANK` before `ZREMRANGEBYRANK` to preview the elements that will be removed.
- Combine `ZREMRANGEBYRANK` with other sorted set commands to manage your dataset efficiently.

## Common Mistakes

- Using incorrect rank values: Ensure the `start` and `stop` parameters are within the existing ranks of the sorted set.
- Misunderstanding ranks vs. scores: `ZREMRANGEBYRANK` operates on ranks, not scores.

## FAQs

**Q: What happens if `start` and `stop` specify an empty range?**
A: No elements are removed, and the command returns 0.

**Q: Can negative indices be used for `start` and `stop`?**
A: Yes, similar to Python slice notation, -1 refers to the last element, -2 to the second last, and so on.
