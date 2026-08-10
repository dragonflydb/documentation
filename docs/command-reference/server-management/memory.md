---
description: Learn how to use Redis MEMORY command to fetch information on memory.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY

<PageTitle title="Redis MEMORY Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY

**Time complexity:** Depends on subcommand.

**ACL categories:** @slow, @read

This is a container command for memory introspection and management commands.

## Subcommands

- [`MEMORY DECOMMIT`](./memory-decommit.md): Return freed memory to the operating system, or
  flush the tiered-storage cool queue.
- [`MEMORY DEFRAGMENT`](./memory-defragment.md): Move allocations out of sparsely used pages.
- [`MEMORY HELP`](./memory-help.md): List available `MEMORY` subcommands.
- [`MEMORY MALLOC-STATS`](./memory-malloc-stats.md): Return allocator statistics.
- [`MEMORY STATS`](./memory-stats.md): Return Dragonfly memory statistics.
- [`MEMORY USAGE`](./memory-usage.md): Return the memory used by a key.
