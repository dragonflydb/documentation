---
description: Get all the fields in a hash
---

# HKEYS

## Syntax

    HKEYS key

**Time complexity:** O(N) where N is the size of the hash.

**ACL categories:** @read, @hash, @slow

Returns all field names in the hash stored at `key`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of fields in the hash, or an empty list when `key` does
not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HKEYS myhash
1) "field1"
2) "field2"
```
