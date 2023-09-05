---
description: Deletes a value
---

# JSON.FORGET

## Syntax

    JSON.FORGET key [path]

**Time complexity:** O(N) when path is evaluated to a single value where N is the size of the deleted value, O(N) when path is evaluated to multiple values, where N is the size of the key

**ACL categories:** @json

See `JSON.DEL`.
