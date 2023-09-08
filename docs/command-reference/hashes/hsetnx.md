---
description: Set the value of a hash field, only if the field does not exist
---

# HSETNX

## Syntax

    HSETNX key field value

**Time complexity:** O(1)

**ACL categories:** @read, @hash, @fast

Sets `field` in the hash stored at `key` to `value`, only if `field` does not
yet exist.
If `key` does not exist, a new key holding a hash is created.
If `field` already exists, this operation has no effect.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers), specifically:

* `1` if `field` is a new field in the hash and `value` was set.
* `0` if `field` already exists in the hash and no operation was performed.

## Examples

```shell
dragonfly> HSETNX myhash field "Hello"
(integer) 1
dragonfly> HSETNX myhash field "World"
(integer) 0
dragonfly> HGET myhash field
"Hello"
```
