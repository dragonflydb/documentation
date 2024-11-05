---
description: Learn how to use the Redis ZADD command to add members to sorted sets with ease, plus expert tips beyond the official Redis docs.
---

import PageTitle from '@site/src/components/PageTitle';

# ZADD

<PageTitle title="Redis ZADD Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZADD` command is used to add one or more members to a sorted set, or update the score of members that already exist in the set.
Each member is associated with a score, and the set is ordered by these scores in ascending order.
`ZADD` is commonly employed in ranking systems, leaderboards, and other applications where maintaining a sorted collection is required.

## Syntax

```shell
ZADD key [NX|XX] [CH] [INCR] score member [score member ...]
```

- **Time complexity:** O(log(N)) for each item added, where N is the number of elements in the sorted set.
- **ACL categories:** @write, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set.
- `NX`: Only add the member if it does not already exist.
- `XX`: Only update the member's score if it already exists.
- `CH`: Return the number of elements changed (not just added).
- `INCR`: Increment the score of the member instead of setting it.
- `score`: The numeric value associated with the member.
- `member`: The string representing the member to be added to the sorted set.

## Return Values

- By default, `ZADD` returns the number of members added to the sorted set (excluding members whose score was updated).
- If used with the `CH` option, `ZADD` returns the number of elements added or updated.

## Code Examples

### Basic Example

Adding scores for members in a sorted set:

```shell
dragonfly$> ZADD myzset 10 "player1" 20 "player2" 15 "player3"
(integer) 3
```

In this example, three members (`"player1"`, `"player2"`, and `"player3"`) are added to the sorted set `myzset` with their respective scores (10, 20, and 15).

### Update an Existing Member’s Score

Updating the score of an already existing member:

```shell
dragonfly$> ZADD myzset 25 "player1"
(integer) 0  # No new members added, only score updated.
```

The member `"player1"` already exists, so `ZADD` only updates its score to 25, and the return value remains `0` as no new members were added.

### Conditional Add (`NX`) and Update (`XX`) Flags

Using the `NX` and `XX` flags to conditionally add or update members:

```shell
dragonfly$> ZADD myzset NX 30 "player4"
(integer) 1  # Added because "player4" did not previously exist.

dragonfly$> ZADD myzset XX 40 "player1"
(integer) 0  # Updated the score of "player1", no new members were added.
```

- In the first command, `NX` ensures `"player4"` is only added if it does not already exist.
- In the second command, `XX` ensures `"player1"` is only updated if it already exists.

### Using `INCR` to Increment a Score

Incrementing a score instead of setting it to a new value:

```shell
dragonfly$> ZADD myzset INCR 5 "player1"
"30"  # The score of "player1" was incremented by 5, resulting in a new score of 30.
```

In this example, the `INCR` option increments the existing score of `"player1"` by 5.

### Change Reporting with `CH`

Using the `CH` flag to report changes:

```shell
dragonfly$> ZADD myzset CH 50 "player5" 30 "player3"
(integer) 2  # Two elements were affected: "player5" was added, and "player3"'s score was updated.
```

The `CH` flag ensures that `ZADD` returns the number of members that were added or had their score updated.

## Best Practices

- Use the `NX` flag if you want to ensure no updates are made to existing members, and members are only added if they do not already exist.
- Use the `XX` flag when you want to update scores without accidentally adding new members to the sorted set.
- Consider using the `CH` option if you need to know exactly how many items were either added or had their scores updated.
- Use the `INCR` option to adjust existing scores rather than replacing them, making it useful in scenarios like games or leaderboards where scores need to accumulate over time.

## Common Mistakes

- Using the `NX` and `XX` flags together, which will result in no members being added or updated. These flags are mutually exclusive.
- Forgetting that `members` in a sorted set must have unique identifiers. Adding a new score for an existing member will update that member’s score rather than creating a duplicate.
- Not understanding that `ZADD` modifies the sorted set’s order based on the updated score when a member is updated.

## FAQs

### What happens if I specify `INCR` but there is no existing score for the member?

If `INCR` is used and the member does not exist, `ZADD` treats the initial score as `0` and then increments it by the provided value.

### Can I use negative scores in `ZADD`?

Yes, scores can be negative in `ZADD`. The command will still order the members based on score, with lower (including negative) values appearing earlier in the sorted set.

### Does `ZADD` overwrite an existing member?

Yes, if a member already exists in a sorted set and `ZADD` is executed without any special flags like `NX`, the score associated with the existing member will be updated to the new value.
