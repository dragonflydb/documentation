---
description: Learn how to use Redis ZSCORE command to get the score associated with the given element in a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZSCORE

<PageTitle title="Redis ZSCORE Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

The `ZSCORE` command in Redis is used to retrieve the score associated with a member in a sorted set. This command is particularly useful in scenarios where you need to know the ranking or priority of an element within a collection, such as leaderboard applications, task scheduling systems, or any system implementing priority queues.

## Syntax

```plaintext
ZSCORE key member
```

## Parameter Explanations

- `key`: The name of the sorted set where the member is stored.
- `member`: The specific member whose score you want to retrieve.

## Return Values

- If the member exists in the sorted set, the command returns its score as a string.
- If the member does not exist, it returns `nil`.

Example Outputs:

- Member exists: `"3.14"`
- Member does not exist: `(nil)`

## Code Examples

```cli
dragonfly> ZADD myzset 1 "a"
(integer) 1
dragonfly> ZADD myzset 2 "b"
(integer) 1
dragonfly> ZADD myzset 3 "c"
(integer) 1
dragonfly> ZSCORE myzset "b"
"2"
dragonfly> ZSCORE myzset "d"
(nil)
```

## Best Practices

- Ensure that the `key` you're querying actually exists and is a sorted set to avoid type errors.
- Regularly monitor your sorted sets for outliers in scores that may indicate erroneous data.

## Common Mistakes

- Attempting to use `ZSCORE` on a key that is not a sorted set will result in an error.
- Querying for a member that doesn't exist in the specified sorted set will return `nil`, which should be handled appropriately in your application logic.

## FAQs

**Q: What happens if the key does not exist?**
A: If the key does not exist, the command returns `nil`.

**Q: Can scores be negative or floating-point numbers?**
A: Yes, scores in Redis sorted sets can be negative or floating-point numbers.
