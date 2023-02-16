---
description: Determine if a hash field exists
---

# HEXISTS

## Syntax

    HEXISTS key field

**Time complexity:** O(1)

Returns if `field` is an existing field in the hash stored at `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if the hash contains `field`.
* `0` if the hash does not contain `field`, or `key` does not exist.

## Examples

```cli
HSET myhash field1 "foo"
HEXISTS myhash field1
HEXISTS myhash field2
```
