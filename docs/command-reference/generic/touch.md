---
description: Alters the last access time of a key(s). Returns the number of
  existing keys specified.
---

# TOUCH

## Syntax

    TOUCH key [key ...]

**Time complexity:** O(N) where N is the number of keys that will be touched.

Alters the last access time of a key(s).
A key is ignored if it does not exist.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): The number of keys that were touched.

## Examples

```cli
SET key1 "Hello"
SET key2 "World"
TOUCH key1 key2
```
