---
description: Get the values of all the given hash fields
---

# HMGET

## Syntax

    HMGET key field [field ...]

**Time complexity:** O(N) where N is the number of fields being requested.

Returns the values associated with the specified `fields` in the hash stored at
`key`.

For every `field` that does not exist in the hash, a `nil` value is returned.
Because non-existing keys are treated as empty hashes, running `HMGET` against
a non-existing `key` will return a list of `nil` values.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of values associated with the given fields, in the same
order as they are requested.

```cli
HSET myhash field1 "Hello"
HSET myhash field2 "World"
HMGET myhash field1 field2 nofield
```
