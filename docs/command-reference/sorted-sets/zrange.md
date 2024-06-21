---
description: Learn to use Redis ZRANGE command to fetch elements in a specific range from a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGE

<PageTitle title="Redis ZRANGE Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

The `ZRANGE` command in Redis is used to return a specified range of elements in a sorted set, sorted by their score. This command is commonly used when you need to retrieve data in a specific order, such as leaderboard rankings, paginated data views, or any scenario where ordered data retrieval is necessary.

## Syntax

```cli
ZRANGE key start stop [WITHSCORES]
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **start**: The starting index (0-based). Negative indices can be used to start from the end of the sorted set.
- **stop**: The stopping index (inclusive). Negative indices can be used to indicate positions from the end of the sorted set.
- **[WITHSCORES]**: An optional parameter that, if provided, will include scores along with the returned elements.

## Return Values

- Without `WITHSCORES`: A list of elements in the specified range.
- With `WITHSCORES`: A list containing elements and their scores, alternating between element and score.

### Examples:

- Without `WITHSCORES`:

  ```cli
  dragonfly> ZRANGE myset 0 -1
  1) "member1"
  2) "member2"
  3) "member3"
  ```

- With `WITHSCORES`:
  ```cli
  dragonfly> ZRANGE myset 0 -1 WITHSCORES
  1) "member1"
  2) "1.0"
  3) "member2"
  4) "2.0"
  5) "member3"
  6) "3.0"
  ```

## Code Examples

```cli
dragonfly> ZADD myset 1 "one" 2 "two" 3 "three"
(integer) 3

dragonfly> ZRANGE myset 0 -1
1) "one"
2) "two"
3) "three"

dragonfly> ZRANGE myset 0 -1 WITHSCORES
1) "one"
2) "1"
3) "two"
4) "2"
5) "three"
6) "3"
```

## Best Practices

- Use negative indices for flexible range queries. For example, `ZRANGE myset -3 -1` retrieves the last three elements.
- When using `WITHSCORES`, ensure your application logic correctly handles the alternating element-score pairs.

## Common Mistakes

- Forgetting that the `stop` index is inclusive, which might lead to off-by-one errors.
- Misinterpreting negative indices and inadvertently retrieving the wrong range of elements.

## FAQs

**Q: Can `ZRANGE` be used to paginate through a large sorted set?**

A: Yes, by specifying appropriate `start` and `stop` indices, `ZRANGE` can be used to implement pagination efficiently.

**Q: What happens if the `start` or `stop` indices are out of the range of the sorted set?**

A: Redis will automatically adjust out-of-range indices to fit within the boundaries of the sorted set, ensuring the command does not fail but returns an empty list if the range is invalid.
