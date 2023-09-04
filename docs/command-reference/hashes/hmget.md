---
description: Get the values of all the given hash fields
---

# HMGET

## Syntax

    HMGET key field [field ...]

**Time complexity:** O(N) where N is the number of fields being requested.

**ACL categories:** @read, @hash, @fast

Returns the values associated with the specified `fields` in the hash stored at
`key`.

For every `field` that does not exist in the hash, a `nil` value is returned.
Because non-existing keys are treated as empty hashes, running `HMGET` against
a non-existing `key` will return a list of `nil` values.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of values associated with the given fields, in the same
order as they are requested.

```shell
dragonfly> HSET myhash field1 "Hello"
(integer) 1
dragonfly> HSET myhash field2 "World"
(integer) 1
dragonfly> HMGET myhash field1 field2 nofield
1) "Hello"
2) "World"
3) (nil)
```
