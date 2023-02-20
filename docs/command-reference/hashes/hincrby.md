---
description: Increment the integer value of a hash field by the given number
---

# HINCRBY

## Syntax

    HINCRBY key field increment

**Time complexity:** O(1)

Increments the number stored at `field` in the hash stored at `key` by
`increment`.
If `key` does not exist, a new key holding a hash is created.
If `field` does not exist the value is set to `0` before the operation is
performed.

The range of values supported by `HINCRBY` is limited to 64 bit signed integers.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the value at `field` after the increment operation.

## Examples

Since the `increment` argument is signed, both increment and decrement
operations can be performed:

```shell
dragonfly> HSET myhash field 5
(integer) 1
dragonfly> HINCRBY myhash field 1
(integer) 6
dragonfly> HINCRBY myhash field -1
(integer) 5
dragonfly> HINCRBY myhash field -10
(integer) -5
```
