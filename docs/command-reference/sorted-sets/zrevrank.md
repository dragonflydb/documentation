---
description: Learn how to use Redis ZREVRANK to determine the index of a member in a sorted set, with scores ordered from high to low.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANK

<PageTitle title="Redis ZREVRANK Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

The `ZREVRANK` command in Redis returns the rank of a member in a sorted set, with the scores ordered from high to low. It is particularly useful for reverse ranking scenarios, such as leaderboard systems where you want to know the position of a participant based on their score.

## Syntax

```
ZREVRANK key member
```

## Parameter Explanations

- `key`: The name of the sorted set.
- `member`: The member whose rank you wish to retrieve.

These parameters are essential for identifying which sorted set and member you are querying.

## Return Values

- **Integer**: The rank of the member (0-based index).
- **nil**: If the member does not exist within the sorted set.

### Example Outputs:

- `(integer) 0` when the member is the highest-scoring member.
- `(nil)` when the member is not found in the sorted set.

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREVRANK myzset "one"
(integer) 2
dragonfly> ZREVRANK myzset "three"
(integer) 0
dragonfly> ZREVRANK myzset "four"
(nil)
```

## Best Practices

- Ensure that the sorted set (`key`) exists before calling `ZREVRANK` to avoid unnecessary nil results.
- Use this command in operations where reverse ranking based on scores is critical, like high-score tables in gaming applications.

## Common Mistakes

- Misinterpreting the 0-based index: A rank of `(integer) 0` means the member has the highest score.
- Forgetting that `ZREVRANK` returns `nil` if the member does not exist, which can lead to unhandled exceptions in some applications.

## FAQs

**Q: What happens if the sorted set does not exist?**

A: The command will simply return `nil`, indicating that the member was not found.

**Q: Can `ZREVRANK` handle negative scores?**

A: Yes, `ZREVRANK` ranks members based on their scores regardless of whether the scores are positive or negative.
