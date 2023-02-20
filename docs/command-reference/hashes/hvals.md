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

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HVALS myhash
1) "Hello"
2) "World"
```
