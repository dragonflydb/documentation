---
description: Add multiple sets and store the resulting set in a key
---

# SUNIONSTORE

## Syntax

    SUNIONSTORE destination key [key ...]

**Time complexity:** O(N) where N is the total number of elements in all given sets.

This command is equal to `SUNION`, but instead of returning the resulting set,
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
SUNIONSTORE key key1 key2
SMEMBERS key
```
