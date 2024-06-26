---
description: ⚡ Better than official Redis docs ⚡ Learn how to use Redis ZRANK command to determine the index of a member in a sorted set, with scores ordered from low to high.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANK

<PageTitle title="Redis ZRANK Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

`ZRANK` is used to determine the rank (or index) of a member in a sorted set, ordered from the lowest to highest score. This command is commonly used when you need to retrieve the position of an element within a leaderboard or any application that requires ranking.

## Syntax

```plaintext
ZRANK key member
```

## Parameter Explanations

- `key`: The name of the sorted set.

  - Type: String
  - Example: `"mySortedSet"`

- `member`: The member whose rank you want to determine.
  - Type: String
  - Example: `"player1"`

## Return Values

- **Integer**: The rank of the member, with 0 being the first rank.
- **nil**: If the member does not exist in the sorted set.

### Examples:

- Member exists:
  ```plaintext
  (integer) 2
  ```
- Member does not exist:
  ```plaintext
  (nil)
  ```

## Code Examples

```cli
dragonfly> ZADD mySortedSet 10 "Alice"
(integer) 1
dragonfly> ZADD mySortedSet 20 "Bob"
(integer) 1
dragonfly> ZADD mySortedSet 15 "Charlie"
(integer) 1
dragonfly> ZRANK mySortedSet "Charlie"
(integer) 1
dragonfly> ZRANK mySortedSet "Bob"
(integer) 2
dragonfly> ZRANK mySortedSet "Dave"
(nil)
```

## Best Practices

- Ensure that the `key` exists and is of type sorted set to avoid unexpected errors.
- Regularly remove members no longer needed to maintain optimal performance.

## Common Mistakes

- Using `ZRANK` on a key that is not a sorted set will result in an error.
- Forgetting that ranks are zero-based, which can lead to off-by-one errors in calculations.

## FAQs

**Q: What happens if I use `ZRANK` on a key that doesn't exist?**
A: Redis will return `nil`, indicating that the member does not exist in the set.

**Q: Can `ZRANK` work with scores that are equal?**
A: Yes, but the rank is determined by the lexicographical order of members with the same score.
