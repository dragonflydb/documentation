---
description: Incrementally iterate Set elements
---

# SSCAN

## Syntax

    SSCAN key cursor [MATCH pattern] [COUNT count]

**Time complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**ACL categories:** @read, @set, @slow

See `SCAN` for `SSCAN` documentation.
