---
description: Get all the members in a set
---

# SMEMBERS

## Syntax

    SMEMBERS key

**Time complexity:** O(N) where N is the set cardinality.

**ACL categories:** @read, @set, @slow

Returns all the members of the set value stored at `key`.

This has the same effect as running `SINTER` with one argument `key`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): all elements of the set.

## Examples

```shell
dragonfly> SADD myset "Hello"
(integer) 1
dragonfly> SADD myset "World"
(integer) 1
dragonfly> SMEMBERS myset
1) "Hello"
2) "World"
```
