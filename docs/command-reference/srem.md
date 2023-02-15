---
description: Remove one or more members from a set
---

# SREM

## Syntax

    SREM key member [member ...]

**Time complexity:** O(N) where N is the number of members to be removed.

Remove the specified members from the set stored at `key`.
Specified members that are not a member of this set are ignored.
If `key` does not exist, it is treated as an empty set and this command returns
`0`.

An error is returned when the value stored at `key` is not a set.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of members that were removed from the set, not
including non existing members.

## Examples

```cli
SADD myset "one"
SADD myset "two"
SADD myset "three"
SREM myset "one"
SREM myset "four"
SMEMBERS myset
```
