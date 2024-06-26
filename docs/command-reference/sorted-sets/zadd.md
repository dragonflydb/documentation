---
description: ⚡ Better than official Redis docs ⚡ Learn how to use Redis ZADD command to add a member to a sorted set with a given score.
---

import PageTitle from '@site/src/components/PageTitle';

# ZADD

<PageTitle title="Redis ZADD Command (Documentation) | Dragonfly" />

## Introduction and Use Case(s)

`ZADD` adds one or more members to a sorted set, or updates the score of existing members. Sorted sets are like regular sets, but with an associated score for each member that determines their order. Common use cases include leaderboards, priority queues, and any scenario requiring ordered data retrieval.

## Syntax

```cli
ZADD key [NX|XX] [CH] [INCR] score member [score member ...]
```

## Parameter Explanations

- `key`: The name of the sorted set.
- `NX`: Only add new elements. Do not update existing elements.
- `XX`: Only update existing elements. Do not add new elements.
- `CH`: Modify the return value from the number of new elements added to the total number of elements changed (new and updated).
- `INCR`: Increment the score of the specified member by the given amount. This option is only allowed to be used with a single `score`/`member` pair.
- `score`: The score to associate with the member.
- `member`: The member to add to the sorted set.

## Return Values

- Without `CH`, returns the number of new elements added to the sorted set.
- With `CH`, returns the number of elements added or updated.
- If used with `INCR`, returns the new score of the member.

### Examples:

1. Adding new members:

   ```cli
   dragonfly> ZADD myzset 1 "one" 2 "two"
   (integer) 2
   ```

2. Updating a member's score:

   ```cli
   dragonfly> ZADD myzset 3 "two"
   (integer) 0
   ```

3. Using `CH` option:

   ```cli
   dragonfly> ZADD myzset CH 4 "three"
   (integer) 1
   ```

4. Incrementing a member's score:
   ```cli
   dragonfly> ZADD myzset INCR 2 "one"
   "3"
   ```

## Code Examples

```cli
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 0
dragonfly> ZRANGE myzset 0 -1 WITHSCORES
1) "one"
2) "1"
3) "two"
4) "2"
```

## Best Practices

- Use `NX` and `XX` options to ensure you are either adding new members or updating existing ones without mixing both operations.
- For large bulk inserts where no members' scores need to be incremented, avoid using `INCR`.

## Common Mistakes

- Misunderstanding the `CH` option: It changes the return value to count all changes, not just additions.
- Using `INCR` with multiple `score`/`member` pairs, which is invalid.

## FAQs

**Q: What happens if I use `NX` and `XX` together?**

A: Using both `NX` and `XX` together is contradictory and will result in an error.

**Q: Can I increment the score of multiple members at once?**

A: No, the `INCR` option can only be used with a single `score`/`member` pair.
