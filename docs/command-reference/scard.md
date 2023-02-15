---
description: Get the number of members in a set
---

# SCARD

## Syntax

    SCARD key

**Time complexity:** O(1)

Returns the set cardinality (number of elements) of the set stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the cardinality (number of elements) of the set, or `0` if `key`
does not exist.

## Examples

```cli
SADD myset "Hello"
SADD myset "World"
SCARD myset
```
