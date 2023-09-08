---
description: Get the length of the value of a hash field
---

# HSTRLEN

## Syntax

    HSTRLEN key field

**Time complexity:** O(1)

**ACL categories:** @read, @hash, @fast

Returns the string length of the value associated with `field` in the hash stored at `key`. If the `key` or the `field` do not exist, 0 is returned.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the string length of the value associated with `field`, or zero when `field` is not present in the hash or `key` does not exist at all.

## Examples

```shell
dragonfly> HMSET myhash f1 HelloWorld f2 99 f3 -256
"OK"
dragonfly> HSTRLEN myhash f1
(integer) 10
dragonfly> HSTRLEN myhash f2
(integer) 2
dragonfly> HSTRLEN myhash f3
(integer) 4
```
