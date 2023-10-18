---
description:  Learn how to incrementally iterate over a collection using Redis SSCAN command.
---

import PageTitle from '@site/src/components/PageTitle';

# SSCAN

<PageTitle title="Redis SSCAN Command (Documentation) | Dragonfly" />

## Syntax

    SSCAN key cursor [MATCH pattern] [COUNT count]

**Time complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**ACL categories:** @read, @set, @slow

See `SCAN` for `SSCAN` documentation.
