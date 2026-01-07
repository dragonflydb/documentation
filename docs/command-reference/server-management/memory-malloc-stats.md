---
description:  Learn how to use Redis MEMORY MALLOC-STATS command to retrieve memory allocator stats.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY MALLOC-STATS

<PageTitle title="Redis MEMORY MALLOC-STATS Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY MALLOC-STATS

**Time complexity:** Depends on how much memory is allocated, could be slow

**ACL categories:** @slow

The `MEMORY MALLOC-STATS` command provides an internal statistics report from
the memory allocator.

## Return

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the memory allocator's internal statistics report
