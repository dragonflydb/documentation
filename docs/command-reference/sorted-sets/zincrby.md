---
description: Learn to use the Redis ZINCRBY command to increment the score of a member in a sorted set, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZINCRBY

<PageTitle title="Redis ZINCRBY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `ZINCRBY` command in Redis is used to increment the score of a member in a sorted set (zset) by a specified amount. If the member does not exist, it will be added with the increment as its score. This command is particularly useful for scenarios such as leaderboards, where you need to adjust scores dynamically based on user activity or other metrics.

## Syntax

```cli
ZINCRBY key increment member
```

## Parameter Explanations

- **key**: The name of the sorted set.
- **increment**: A floating-point number that represents the value to be added to the member's score.
- **member**: The specific member whose score you want to increment.

## Return Values

`ZINCRBY` returns the new score of the member after the increment.

Example:

```cli
(integer) 3.5
```

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZINCRBY myzset 2 "one"
"3"
dragonfly> ZINCRBY myzset -1 "one"
"2"
dragonfly> ZINCRBY myzset 5 "two"
"5"
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "one"
2) "2"
3) "two"
4) "5"
```

## Best Practices

- Always ensure the member exists before performing large increments, especially in critical applications, to avoid unexpected behaviors.
- Use floating-point increments for precise adjustments, particularly in financial or gaming applications where minute differences matter.

## Common Mistakes

- Providing a non-numeric value for the increment parameter, which will result in an error.
- Forgetting that if the member does not exist, it will be added with the increment as the initial score, which might lead to unintended data entries.

## FAQs

### What happens if the member doesn't exist in the sorted set?

If the member does not exist, `ZINCRBY` will add it to the sorted set with the increment as its score.

### Can I decrement the score using ZINCRBY?

Yes, you can decrement the score by providing a negative value for the increment.
