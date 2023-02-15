---
description: Get the number of references to the value of the key
---

# OBJECT REFCOUNT

## Syntax

    OBJECT REFCOUNT key

**Time complexity:** O(1)

This command returns the reference count of the stored at `<key>`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers)

The number of references.