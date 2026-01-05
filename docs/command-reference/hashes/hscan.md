---
description: "Learn how to use Redis HSCAN command to iteratively scan over a hash. Improve your data access strategy with this command."
---

import PageTitle from '@site/src/components/PageTitle';

# HSCAN

<PageTitle title="Redis HSCAN Command (Documentation) | Dragonfly" />

## Syntax

    HSCAN key cursor [MATCH pattern] [COUNT count]

**Time complexity:** O(1) for every call. O(N) for a complete iteration, including enough command calls for the cursor to return back to 0. N is the number of elements inside the collection.

**ACL categories:** @read, @hash, @slow

See [SCAN](../generic/scan) for `HSCAN` documentation.
