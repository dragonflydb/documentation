---
description: Learn how to use Redis ZREVRANGE command to return a range of members in a sorted set, by index, with scores ordered from high to low.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANGE

<PageTitle title="Redis ZREVRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`ZREVRANGE` is a Redis command used to return a range of members in a sorted set, ordered from the highest to the lowest score. It is particularly useful for scenarios where you need to retrieve top-ranking items or reverse-order lists, such as leaderboards, ranking systems, or any application requiring sorted data retrieval in descending order.

## Syntax

```plaintext
ZREVRANGE key start stop [WITHSCORES]
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **start**: The starting rank position (0-based index) from which to begin retrieving elements.
- **stop**: The ending rank position up to which to retrieve elements. A negative index can be used to count from the end of the sorted set (-1 being the last element).
- **WITHSCORES**: Optional. When provided, it includes the scores of the returned elements.

## Return Values

- Without `WITHSCORES`: Returns a list of elements in the specified range, ordered from the highest to the lowest score.
- With `WITHSCORES`: Returns a list of elements with their scores in the specified range, ordered from the highest to the lowest score.

### Examples:

Without `WITHSCORES`:

```cli
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZREVRANGE myzset 0 -1
1) "three"
2) "two"
3) "one"
```

With `WITHSCORES`:

```cli
dragonfly> ZREVRANGE myzset 0 -1 WITHSCORES
1) "three"
2) "3"
3) "two"
4) "2"
5) "one"
6) "1"
```

## Code Examples

Using CLI:

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREVRANGE myzset 0 -1
1) "three"
2) "two"
3) "one"
dragonfly> ZREVRANGE myzset 1 2 WITHSCORES
1) "two"
2) "2"
3) "one"
4) "1"
dragonfly> ZREVRANGE myzset 0 0
1) "three"
```

## Best Practices

- Consider using pagination by adjusting the `start` and `stop` parameters to manage large sets.
- Use `WITHSCORES` only when necessary to minimize data transfer and improve performance.

## Common Mistakes

- Not accounting for zero-based indexing while specifying `start` and `stop`.
- Using very large ranges without considering performance impacts on large sets.

## FAQs

### How does ZREVRANGE differ from ZRANGE?

While `ZRANGE` returns elements in ascending order of scores, `ZREVRANGE` returns them in descending order.

### Can I use negative indices with ZREVRANGE?

Yes, negative indices can be used to specify ranges relative to the end of the sorted set.
