---
description: Subtract multiple sets and store the resulting set in a key
---

# SDIFFSTORE

## Syntax

    SDIFFSTORE destination key [key ...]

**Time complexity:** O(N) where N is the total number of elements in all given sets.

**ACL categories:** @write, @set, @slow

This command is equal to `SDIFF`, but instead of returning the resulting set, it
is stored in `destination`.

If `destination` already exists, it is overwritten.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements in the resulting set.

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
dragonfly> SDIFFSTORE key key1 key2
(integer) 2
dragonfly> SMEMBERS key
1) "b"
2) "a"
```
