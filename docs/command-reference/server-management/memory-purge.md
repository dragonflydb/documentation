---
description: Ask the allocator to release memory
---

# MEMORY PURGE

## Syntax

    MEMORY PURGE 

**Time complexity:** Depends on how much memory is allocated, could be slow

The `MEMORY PURGE` command attempts to purge dirty pages so these can be
reclaimed by the allocator.

This command is currently implemented only when using **jemalloc** as an
allocator, and evaluates to a benign NOOP for all others.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)
