---
description:  Learn how to use the Dragonfly MEMORY DEFRAGMENT command to reclaim memory from sparsely used pages on demand.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY DEFRAGMENT

<PageTitle title="Dragonfly MEMORY DEFRAGMENT Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY DEFRAGMENT [threshold]

**Time complexity:** O(N) where N is the number of entries visited during the invocation, which is bounded by an internal time budget per thread.

**ACL categories:** @read, @slow

The `MEMORY DEFRAGMENT` command runs a defragmentation pass on demand and returns a report
describing what was scanned. This command is Dragonfly-specific.

Values are allocated from fixed-size memory pages. When keys are deleted or values shrink, the
remaining live objects can end up scattered across many partially used pages, so the process keeps
memory committed to the operating system (visible as `used_memory_rss` in
[`INFO`](./info.md)) that is no longer backing data. Defragmentation walks the entries of a shard
and reallocates the objects that sit on sparsely used pages, which allows the allocator to release
those pages back.

Dragonfly already runs this as a background task, gated by the `--mem_defrag_threshold` and
`--mem_defrag_waste_threshold` flags and evaluated every `--mem_defrag_check_sec_interval` seconds.
`MEMORY DEFRAGMENT` triggers the same relocation logic immediately, without those gating checks,
and reports the page statistics it collected along the way.

## Threshold

The optional `threshold` is a ratio between 0 and 1: a page is a candidate for relocation when the
ratio of its used blocks to its capacity is below the threshold. A lower value moves objects only
out of very sparse pages, while a higher value is more aggressive and relocates objects out of
pages that are already reasonably well utilized.

When `threshold` is omitted, the value of the `--mem_defrag_page_utilization_threshold` flag is
used, which defaults to `0.8`. The threshold in effect for the invocation is echoed back as a
percentage in the first line of the report.

## Incremental behavior

The command runs on every shard thread in parallel, and each thread stops once it exhausts a small
time budget, so a single invocation scans only part of the keyspace. Each shard keeps a scan
cursor, and the next invocation resumes from where the previous one stopped. Run the command
repeatedly to cover a large keyspace.

When a shard completes a full pass over its data, the following invocation resets that shard's
cursor and reports no pages for it — an empty `[Shard n]` section with zero counters. The
invocation after that starts a new pass from the beginning.

## Return

[Verbatim string reply](https://valkey.io/topics/protocol/#verbatim-strings): a report of the pages
and objects inspected during the invocation.

| Field | Description |
| --- | --- |
| `Page usage threshold` | The threshold in effect, as a percentage. |
| `Pages scanned` | Number of distinct pages inspected. |
| `Pages marked for reallocation` | Pages found below the threshold, whose objects were moved. |
| `Pages full` | Pages with no free blocks, so there is nothing to reclaim from them. |
| `Pages reserved for malloc` | Pages backing generic allocations rather than data, which are skipped. |
| `Pages skipped due to heap mismatch` | Pages owned by another thread's heap, which cannot be relocated from this thread. |
| `Pages with usage above threshold` | Pages that were neither full nor below the threshold. |
| `Objects skipped (do not require defragmentation)` | Entries whose payload is stored inline and therefore never needs to be moved. |
| `Objects skipped (do not support defragmentation)` | Entries whose value type has no defragmentation support, such as streams. |
| `[Shard n]` | Per-shard distribution of block usage across the pages that were above the threshold but not full. |

Page counts are approximations produced from a probabilistic counter, so they may differ slightly
from the exact number of pages touched.

The per-shard section is useful for tuning the `threshold` argument: if most pages sit just above
the current threshold, raising it makes the next pass reclaim more memory.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `threshold` is not a valid
floating point number.

## Examples

Reclaiming memory after a large deletion. In this example an instance running with two shards holds
300,000 keys, 70% of which are then deleted:

```shell
dragonfly> DBSIZE
(integer) 90000

dragonfly> INFO memory
# Memory
used_memory:36982288
used_memory_rss:115564544
...

dragonfly> MEMORY DEFRAGMENT
Page usage threshold: 80
Pages scanned: 130
Pages marked for reallocation: 130
Pages full: 0
Pages reserved for malloc: 0
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

dragonfly> INFO memory
# Memory
used_memory:36982288
used_memory_rss:68759552
...
```

The invocation that follows a completed pass resets the scan cursor and reports nothing:

```shell
dragonfly> MEMORY DEFRAGMENT
Page usage threshold: 80
Pages scanned: 0
Pages marked for reallocation: 0
Pages full: 0
Pages reserved for malloc: 0
Pages skipped due to heap mismatch: 0
Pages with usage above threshold: 0
Objects skipped (do not require defragmentation): 0
Objects skipped (do not support defragmentation): 0
[Shard 0]
[Shard 1]
```

Supplying an explicit threshold:

```shell
dragonfly> MEMORY DEFRAGMENT 0.5
Page usage threshold: 50
Pages scanned: 5
Pages marked for reallocation: 0
Pages full: 5
Pages reserved for malloc: 0
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

dragonfly> MEMORY DEFRAGMENT abc
(error) ERR value is not a valid float
```

The cumulative effect of both the background task and this command is tracked by the
`defrag_attempt_total`, `defrag_realloc_total`, and `defrag_task_invocation_total` fields of
[`INFO`](./info.md).

## See also

[`MEMORY`](./memory.md) | [`MEMORY DECOMMIT`](./memory-decommit.md) | [`MEMORY ARENA`](./memory-arena.md) | [`MEMORY MALLOC-STATS`](./memory-malloc-stats.md) | [`MEMORY HELP`](./memory-help.md) | [Server configuration flags](../../managing-dragonfly/flags.md)
