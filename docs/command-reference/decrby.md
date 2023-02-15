---
description: Decrement the integer value of a key by the given number
---

# DECRBY

## Syntax

    DECRBY key decrement

**Time complexity:** O(1)

Decrements the number stored at `key` by `decrement`.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as integer.
This operation is limited to 64 bit signed integers.

See `INCR` for extra information on increment/decrement operations.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the value of `key` after the decrement

## Examples

```cli
SET mykey "10"
DECRBY mykey 3
```
