---
description: Get the number of members in a set
---

# SCARD

## Syntax

    SCARD key

**Time complexity:** O(1)

**ACL categories:** @read, @set, @fast

Returns the set cardinality (number of elements) of the set stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the cardinality (number of elements) of the set, or `0` if `key`
does not exist.

## Examples

```shell
dragonfly> SADD myset "Hello"
(integer) 1
dragonfly> SADD myset "World"
(integer) 1
dragonfly> SCARD myset
(integer) 2
```
