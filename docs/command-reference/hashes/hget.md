---
description: Get the value of a hash field
---

# HGET

## Syntax

    HGET key field

**Time complexity:** O(1)

Returns the value associated with `field` in the hash stored at `key`.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the value associated with `field`, or `nil` when `field` is not
present in the hash or `key` does not exist.

## Examples

```cli
HSET myhash field1 "foo"
HGET myhash field1
HGET myhash field2
```
