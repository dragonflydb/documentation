---
description: Get the number of fields in a hash
---

# HLEN

## Syntax

    HLEN key

**Time complexity:** O(1)

**ACL categories:** @read, @hash, @fast

Returns the number of fields contained in the hash stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): number of fields in the hash, or `0` when `key` does not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HLEN myhash
(integer) 2
```
