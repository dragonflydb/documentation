---
description: Learn how to use Redis ZRANGEBYSCORE which returns elements with scores within a given range in a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANGEBYSCORE

<PageTitle title="Redis ZRANGEBYSCORE Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

The `ZRANGEBYSCORE` command in Redis is used to return the members of a sorted set whose scores fall within a specified range. This command is particularly useful for retrieving elements based on their ranking or priority, such as fetching leaderboard entries, scheduled tasks within a certain time frame, or items with specific score values.

## Syntax

```
ZRANGEBYSCORE key min max [WITHSCORES] [LIMIT offset count]
```

## Parameter Explanations

- `key`: The name of the sorted set.
- `min`: The minimum score (inclusive) of the range.
- `max`: The maximum score (inclusive) of the range.
- `WITHSCORES` (optional): Include this to return the scores of the elements in addition to the elements themselves.
- `LIMIT offset count` (optional): Used to paginate through the results. `offset` specifies the number of elements to skip, and `count` specifies the maximum number of elements to return.

## Return Values

The command returns an array of elements in the specified score range. If `WITHSCORES` is used, the array will alternate between elements and their respective scores.

### Examples:

- Without `WITHSCORES`:
  ```
  ["element1", "element2", "element3"]
  ```
- With `WITHSCORES`:
  ```
  ["element1", "1.0", "element2", "2.0", "element3", "3.0"]
  ```

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZRANGEBYSCORE myzset 1 2
1) "one"
2) "two"
dragonfly> ZRANGEBYSCORE myzset 1 2 WITHSCORES
1) "one"
2) "1"
3) "two"
4) "2"
dragonfly> ZRANGEBYSCORE myzset 2 3 LIMIT 1 1
1) "three"
```

## Best Practices

- Use `WITHSCORES` only when necessary to avoid additional memory overhead.
- Apply the `LIMIT` option for large sorted sets to manage memory usage and improve performance.
- Ensure `min` and `max` are set appropriately to avoid unexpected results.

## Common Mistakes

- Using `min` and `max` incorrectly: Ensure that `min` <= `max`.
- Omitting `WITHSCORES` when scores are needed for further processing, which leads to additional queries.

## FAQs

**Q: Can I use negative scores with `ZRANGEBYSCORE`?**
A: Yes, both `min` and `max` can be negative numbers.

**Q: What happens if no elements fall within the given score range?**
A: An empty array will be returned.

**Q: How does Redis handle non-numeric `min` or `max` values?**
A: Redis will return an error as `min` and `max` must be valid numeric values or special strings like `-inf` and `+inf`.
