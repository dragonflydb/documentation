---
description: Get all the values in a hash
---

# HVALS

## Syntax

    HVALS key

**Time complexity:** O(N) where N is the size of the hash.

Returns all values in the hash stored at `key`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of values in the hash, or an empty list when `key` does
not exist.

## Examples

```cli
HSET myhash field1 "Hello"
HSET myhash field2 "World"
HVALS myhash
```
