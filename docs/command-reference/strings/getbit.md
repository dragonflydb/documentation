---
description: Returns the bit value at offset in the string value stored at key
---

# GETBIT

## Syntax

    GETBIT key offset

**Time complexity:** O(1)

**ACL categories:** @read, @bitmap, @fast

Returns the bit value at _offset_ (zero-indexed) in the string value stored at _key_.

When _offset_ is beyond the string length, the string is assumed to be a
contiguous space with 0 bits.
When _key_ does not exist it is assumed to be an empty string, so _offset_ is
always out of range and the value is also assumed to be a contiguous space with
0 bits.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the bit value stored at _offset_.

## Examples

```shell
dragonfly> SET mykey "\x42"  # 0100'0010
dragonfly> GETBIT mykey 0
(integer) 0
dragonfly> GETBIT mykey 1
(integer) 1
dragonfly> GETBIT mykey 6
(integer) 1
dragonfly> GETBIT mykey 100
(integer) 0
```
