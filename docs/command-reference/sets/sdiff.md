---
description: Subtract multiple sets
---

# SDIFF

## Syntax

    SDIFF key [key ...]

**Time complexity:** O(N) where N is the total number of elements in all given sets.

**ACL categories:** @read, @set, @slow

Returns the members of the set resulting from the difference between the first
set and all the successive sets.

For example:

```
key1 = {a,b,c,d}
key2 = {c}
key3 = {a,c,e}
SDIFF key1 key2 key3 = {b,d}
```

Keys that do not exist are considered to be empty sets.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list with members of the resulting set.

## Examples

```shell
dragonfly> SADD key1 "a"
(integer) 1
dragonfly> SADD key1 "b"
(integer) 1
dragonfly> SADD key1 "c"
(integer) 1
dragonfly> SADD key2 "c"
(integer) 1
dragonfly> SADD key2 "d"
(integer) 1
dragonfly> SADD key2 "e"
(integer) 1
dragonfly> SDIFF key1 key2
1) "b"
2) "a"
```
