---
description: Learn how to use the Dragonfly MEMORY DEFRAGMENT-SEGMENTS command to relocate hash-table segments from sparsely used memory pages.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY DEFRAGMENT-SEGMENTS

<PageTitle title="Dragonfly MEMORY DEFRAGMENT-SEGMENTS Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY DEFRAGMENT-SEGMENTS [threshold]

**Time complexity:** O(N) in the worst case, where N is the number of hash-table directory entries in the selected database. Each shard uses an internal time budget to limit work per invocation.

**ACL categories (Dragonfly v2.0.2):** @read, @slow

This Dragonfly-specific command attempts to relocate the selected database's
primary hash-table segments from sparsely used allocator pages. It is intended
for development, diagnostics, and manual memory investigations.

Hash-table segments hold the buckets used to locate keys. Relocating segments
can make allocator pages available for reuse or release. The command preserves
the keys and values stored in the database. It targets table storage;
[`MEMORY DEFRAGMENT`](./memory-defragment.md) targets allocations belonging to
keys and values.

Only the database selected on the current connection is processed, across its
shards. Use [`SELECT`](./select.md) to choose a different database.

## Threshold

The optional `threshold` must satisfy `0 < threshold <= 1`. A page is eligible
when its used-block ratio is below this value. This measures utilization of the
allocator page containing a segment, not the proportion of occupied buckets
inside the segment.

When omitted, the command uses `--mem_defrag_page_utilization_threshold`, whose
default is `0.8`. The report shows the threshold as a percentage. A higher value
makes more sparsely used pages eligible for relocation.

## Incremental behavior

Each shard keeps a segment scan cursor for the selected database. An invocation
resumes at that cursor and stops when it reaches the end of the table or
exhausts its time budget. A subsequent invocation resumes an unfinished pass or
starts a new pass after a completed one.

Segments that cannot safely be relocated are skipped. The command attempts
relocation but does not guarantee that memory is returned to the operating
system or that `used_memory_rss` decreases.

The work runs concurrently on shard threads and can temporarily monopolize them,
causing high CPU usage and latency spikes. Use the command during low-traffic
periods.

## Return

[Verbatim string reply](https://valkey.io/topics/protocol/#verbatim-strings): a
page-usage report with the same fields as
[`MEMORY DEFRAGMENT`](./memory-defragment.md#return), including the threshold,
pages scanned, pages marked for reallocation, and per-shard utilization summaries.

Page counts are approximate. `Pages marked for reallocation` counts eligible
pages; it is not a count of successfully moved segments or pages released to the
operating system.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `threshold`
is not a valid floating point number, is outside the allowed range, or extra
arguments are supplied.

## Examples

This report was collected on Dragonfly v2.0.2 with two shards, after inserting
10,000 string keys into database 1 and deleting 8,000 of them. The report depends
on allocator state; in this example, no pages were marked for reallocation.

```shell
dragonfly> SELECT 1
OK

dragonfly> DBSIZE
(integer) 2000

dragonfly> MEMORY DEFRAGMENT-SEGMENTS
Page usage threshold: 80
Pages scanned: 2
Pages marked for reallocation: 0
Pages full: 2
Pages reserved for malloc: 2
Pages skipped due to heap mismatch: 0
Pages with usage above threshold: 0
Objects skipped (do not require defragmentation): 0
Objects skipped (do not support defragmentation): 0
[Shard 0]
 50% pages are below 0% block usage
 90% pages are below 0% block usage
 99% pages are below 0% block usage
[Shard 1]
 50% pages are below 0% block usage
 90% pages are below 0% block usage
 99% pages are below 0% block usage
```

Zero is not a valid threshold:

```shell
dragonfly> MEMORY DEFRAGMENT-SEGMENTS 0
(error) ERR Threshold must be between 0 and 1

dragonfly> MEMORY DEFRAGMENT-SEGMENTS abc
(error) ERR value is not a valid float
```

## See also

[`MEMORY DEFRAGMENT`](./memory-defragment.md) | [`MEMORY DECOMMIT`](./memory-decommit.md) | [`MEMORY ARENA`](./memory-arena.md) | [`MEMORY HELP`](./memory-help.md) | [Server configuration flags](../../managing-dragonfly/flags.md)
