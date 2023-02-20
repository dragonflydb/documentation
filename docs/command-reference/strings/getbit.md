---
description: Returns the bit value at offset in the string value stored at key
---

# GETBIT

## Syntax

    GETBIT key offset

**Time complexity:** O(1)

Returns the bit value at _offset_ in the string value stored at _key_.

When _offset_ is beyond the string length, the string is assumed to be a
contiguous space with 0 bits.
When _key_ does not exist it is assumed to be an empty string, so _offset_ is
always out of range and the value is also assumed to be a contiguous space with
0 bits.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the bit value stored at _offset_.

## Examples

```shell
dragonfly> SETBIT mykey 7 1
(integer) 0
dragonfly> GETBIT mykey 0
(integer) 0
dragonfly> GETBIT mykey 7
(integer) 1
dragonfly> GETBIT mykey 100
(integer) 0
```
