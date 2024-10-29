---
description: Learn how to use Redis ZSCORE command to get the score associated with the given element in a sorted set.
---

import PageTitle from '@site/src/components/PageTitle';

# ZSCORE

<PageTitle title="Redis ZSCORE Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZSCORE` command is used to get the score associated with a member in a sorted set.
Each element in a sorted set is ordered according to its score, so this command is especially helpful to query and retrieve a specific element's score efficiently.

## Syntax

```shell
ZSCORE key member
```

- **Time complexity:** O(1)
- **ACL categories:** @read, @sortedset, @fast

## Parameter Explanations

- `key`: The key of the sorted set where the member belongs.
- `member`: The member whose score you want to retrieve.

## Return Values

The command returns the score (as a string) associated with the specified `member`.
If the `member` does not exist within the sorted set, `nil` is returned.

## Code Examples

### Basic Example

Retrieve the score of a specific member from the sorted set:

```shell
dragonfly> ZADD myzset 1 "member1" 2 "member2" 3 "member3"
(integer) 3
dragonfly> ZSCORE myzset "member2"
"2"
```

### Member Not Found

If a `member` is not present in a sorted set, `ZSCORE` will return `nil`:

```shell
dragonfly> ZSCORE myzset "non_existent_member"
(nil)
```

### Score for Members with Decimal Values

Sorted sets can store floating-point scores. The `ZSCORE` command will return such values as strings:

```shell
dragonfly> ZADD myzset 1.5 "memberA" 3.7 "memberB"
(integer) 2
dragonfly> ZSCORE myzset "memberB"
"3.7"
```

## Best Practices

- Use the `ZSCORE` command when you only need to retrieve the score of a single member as it provides a direct and efficient method to perform this query.
- When working with large sorted sets, ensure that looks up for non-existent members won't clutter your application’s logic; handle the `nil` return value accordingly.
- To get multiple scores at once, consider pairing `ZSCORE` with other sorted set operations like `ZRANGE` or `ZSCAN` for more complex queries.

## Common Mistakes

- Expecting `ZSCORE` to return a numeric value. The score is returned as a string, and you'll need to convert it if further numeric operations are necessary.
- Assuming that a negative score means the member is "lower" in the sorted set. The sorted set will order by score, and not necessarily by logic derived from the score’s value.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `ZSCORE` returns `nil`.

### Can I use `ZSCORE` with non-numeric strings as members?

Yes, members in sorted sets are just strings, so they can be any valid string value. However, the scores associated with them must be numeric.
