---
description: Incrementally iterate sorted sets elements and associated scores
---

# ZSCAN

## Syntax

    ZSCAN key cursor [MATCH pattern] [COUNT count]

**Time complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**ACL categories:** @read, @sortedset, @slow

See `SCAN` for `ZSCAN` documentation.
