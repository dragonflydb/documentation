---
description: Show allocator internal stats
---

# MEMORY MALLOC-STATS

## Syntax

    MEMORY MALLOC-STATS 

**Time complexity:** Depends on how much memory is allocated, could be slow

The `MEMORY MALLOC-STATS` command provides an internal statistics report from
the memory allocator.

This command is currently implemented only when using **jemalloc** as an
allocator, and evaluates to a benign NOOP for all others.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the memory allocator's internal statistics report
