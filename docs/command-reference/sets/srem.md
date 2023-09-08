---
description: Remove one or more members from a set
---

# SREM

## Syntax

    SREM key member [member ...]

**Time complexity:** O(N) where N is the number of members to be removed.

**ACL categories:** @write, @set, @fast

Remove the specified members from the set stored at `key`.
Specified members that are not a member of this set are ignored.
If `key` does not exist, it is treated as an empty set and this command returns
`0`.

An error is returned when the value stored at `key` is not a set.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of members that were removed from the set, not
including non existing members.

## Examples

```shell
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SADD myset "three"
(integer) 1
dragonfly> SREM myset "one"
(integer) 1
dragonfly> SREM myset "four"
(integer) 0
dragonfly> SMEMBERS myset
1) "three"
2) "two"
```
