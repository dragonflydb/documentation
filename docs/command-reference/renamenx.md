---
description: Rename a key, only if the new key does not exist
---

# RENAMENX

## Syntax

    RENAMENX key newkey

**Time complexity:** O(1)

Renames `key` to `newkey` if `newkey` does not yet exist.
It returns an error when `key` does not exist.

In Cluster mode, both `key` and `newkey` must be in the same **hash slot**, meaning that in practice only keys that have the same hash tag can be reliably renamed in cluster.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers), specifically:

* `1` if `key` was renamed to `newkey`.
* `0` if `newkey` already exists.

## Examples

```cli
SET mykey "Hello"
SET myotherkey "World"
RENAMENX mykey myotherkey
GET myotherkey
```
