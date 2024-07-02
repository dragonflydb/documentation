---
description: Learn how to use the Redis ZPOPMAX command to remove and return the member with the highest score in a sorted set, plus expert tips beyond the official docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZPOPMAX

<PageTitle title="Redis ZPOPMAX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZPOPMAX` command in Redis is used to remove and return the member with the highest score in a sorted set. It is particularly useful in scenarios where you need to process or consume elements with the highest priority first, such as task scheduling or leaderboard management.

## Syntax

```plaintext
ZPOPMAX key [count]
```

## Parameter Explanations

- **key**: The name of the sorted set from which to pop the member with the highest score.
- **count**: An optional integer that specifies the number of elements to return. If not specified, it defaults to 1.

## Return Values

The command returns an array containing the members and their scores, ordered from the highest to the lowest score.

Examples:

- If `count` is 1 (or not specified), the response will be a two-element array: the member and its score.
- If `count` is greater than 1, the response will be an array containing each member followed by its score.

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one" 2 "two" 3 "three"
(integer) 3
dragonfly> ZPOPMAX myzset
1) "three"
2) "3"
dragonfly> ZPOPMAX myzset 2
1) "two"
2) "2"
3) "one"
4) "1"
```

## Best Practices

- Use `ZPOPMAX` when you need to dequeue items in order of their priority or score.
- Combine `ZPOPMAX` with other commands like `ZADD` to maintain and manipulate your sorted set efficiently.

## Common Mistakes

- Forgetting that `ZPOPMAX` removes the elements from the sorted set. If you only need to view the highest-scoring element, consider using the `ZRANGE` or `ZREVRANGE` command instead.

## FAQs

### Can I use ZPOPMAX on a non-existing key?

Yes, if the key does not exist, `ZPOPMAX` will return an empty array.
