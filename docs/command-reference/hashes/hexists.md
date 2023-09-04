---
description: Determine if a hash field exists
---

# HEXISTS

## Syntax

    HEXISTS key field

**Time complexity:** O(1)

**ACL categories:** @read, @hash, @fast

Returns if `field` is an existing field in the hash stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if the hash contains `field`.
* `0` if the hash does not contain `field`, or `key` does not exist.

## Examples

```shell
dragonfly> HSET myhash field1 "foo"
(integer) 1
dragonfly> HEXISTS myhash field1
(integer) 1
dragonfly> HEXISTS myhash field2
(integer) 0
```
