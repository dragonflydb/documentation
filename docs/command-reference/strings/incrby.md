---
description: Increment the integer value of a key by the given amount
---

# INCRBY

## Syntax

    INCRBY key increment

**Time complexity:** O(1)

Increments the number stored at `key` by `increment`.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as integer.
This operation is limited to 64 bit signed integers.

See `INCR` for extra information on increment/decrement operations.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the value of `key` after the increment

## Examples

```shell
dragonfly> SET mykey "10"
"OK"
dragonfly> INCRBY mykey 5
(integer) 15
```
