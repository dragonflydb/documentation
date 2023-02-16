---
description: Get the number of fields in a hash
---

# HLEN

## Syntax

    HLEN key

**Time complexity:** O(1)

Returns the number of fields contained in the hash stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): number of fields in the hash, or `0` when `key` does not exist.

## Examples

```cli
HSET myhash field1 "Hello"
HSET myhash field2 "World"
HLEN myhash
```
