---
description: Rename a key, only if the new key does not exist
---

# RENAMENX

## Syntax

    RENAMENX key newkey

**Time complexity:** O(1)

Renames `key` to `newkey` if `newkey` does not yet exist.
It returns an error when `key` does not exist.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if `key` was renamed to `newkey`.
* `0` if `newkey` already exists.

## Examples

```shell
dragonfly> SET mykey "Hello"
"OK"
dragonfly> SET myotherkey "World"
"OK"
dragonfly> RENAMENX mykey myotherkey
(integer) 0
dragonfly> GET myotherkey
"World"
```
