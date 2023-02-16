---
description: Intersect multiple sets and store the resulting set in a key
---

# SINTERSTORE

## Syntax

    SINTERSTORE destination key [key ...]

**Time complexity:** O(N*M) worst case where N is the cardinality of the smallest set and M is the number of sets.

This command is equal to `SINTER`, but instead of returning the resulting set,
it is stored in `destination`.

If `destination` already exists, it is overwritten.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of elements in the resulting set.

## Examples

```cli
SADD key1 "a"
SADD key1 "b"
SADD key1 "c"
SADD key2 "c"
SADD key2 "d"
SADD key2 "e"
SINTERSTORE key key1 key2
SMEMBERS key
```
