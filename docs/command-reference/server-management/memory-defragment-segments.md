---
description:  Learn how to use the Dragonfly MEMORY DEFRAGMENT-SEGMENTS command to relocate hash table segments off sparsely used memory pages.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY DEFRAGMENT-SEGMENTS

<PageTitle title="Dragonfly MEMORY DEFRAGMENT-SEGMENTS Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY DEFRAGMENT-SEGMENTS [threshold]

**Time complexity:** O(N) where N is the number of segments visited during the invocation, which is bounded by an internal time budget per thread.

**ACL categories:** @read, @slow

The `MEMORY DEFRAGMENT-SEGMENTS` command relocates the hash table segments of the currently
selected database off sparsely used memory pages, and returns a report describing the pages it
inspected. This command is Dragonfly-specific.

Each shard keeps its keys in a hash table that is built out of fixed-size *segments*. A segment is
itself a single large allocation holding many entries, so segments occupy memory pages just as
values do. [`MEMORY DEFRAGMENT`](./memory-defragment.md) walks the entries of a shard and moves the
*values* that sit on sparsely used pages, but it never moves the table structure itself. When it is
the segments that keep those pages committed, this command is what consolidates them.

The typical cause is a database whose table grew and then released segments — for example after a
[`FLUSHDB`](./flushdb.md) of another database that shared the same pages, or after a large table
shrank. The surviving segments are left scattered, one or two per page, and the allocator cannot
release those pages while a single live segment remains on each.

Unlike value defragmentation, segment relocation has no background counterpart: it happens only
when this command is issued.

## Database scope

The command operates on the database currently selected on the connection, on every shard. Other
databases are left untouched. To defragment several databases, [`SELECT`](./select.md)
each one in turn and run the command again.

## Threshold

The optional `threshold` is a ratio greater than 0 and at most 1: a page is a candidate for
relocation when the ratio of its used blocks to its capacity is below the threshold. A lower value
moves segments only out of very sparse pages, while a higher value is more aggressive. A value of
`1` treats every page that is not completely full as a candidate.

When `threshold` is omitted, the value of the `--mem_defrag_page_utilization_threshold` flag is
used, which defaults to `0.8`. The threshold in effect for the invocation is echoed back as a
percentage in the first line of the report.

## Incremental behavior

The command runs on every shard thread in parallel, and each thread stops once it exhausts a small
time budget, so a single invocation may visit only part of the table. Each database keeps a scan
cursor per shard, and the next invocation resumes from where the previous one stopped. Once a shard
has visited every segment, the cursor wraps around and the following invocation starts a new pass
from the first segment. Flushing the database resets the cursor.

Because of this, the command is meant to be run repeatedly until it reports nothing left to move,
rather than once. A segment that is being read at the moment it is visited cannot be moved either,
since relocating it would invalidate the pointers held into it; such segments are skipped and are
picked up by a later invocation.

## Return

[Verbatim string reply](https://valkey.io/topics/protocol/#verbatim-strings): a report of the pages
inspected during the invocation, in the same format as
[`MEMORY DEFRAGMENT`](./memory-defragment.md).

| Field | Description |
| --- | --- |
| `Page usage threshold` | The threshold in effect, as a percentage. |
| `Pages scanned` | Number of distinct pages inspected. |
| `Pages marked for reallocation` | Pages found below the threshold, whose segments were candidates for moving. |
| `Pages full` | Pages with no free blocks, so there is nothing to reclaim from them. |
| `Pages reserved for malloc` | Pages backing generic allocations rather than data, which are skipped. |
| `Pages skipped due to heap mismatch` | Pages owned by another thread's heap, which cannot be relocated from this thread. |
| `Pages with usage above threshold` | Pages that were neither full nor below the threshold. |
| `Objects skipped (do not require defragmentation)` | Always `0`, as this command inspects segments rather than individual values. |
| `Objects skipped (do not support defragmentation)` | Always `0`, for the same reason. |
| `[Shard n]` | Per-shard distribution of block usage across the pages that were above the threshold but not full. |

Page counts are approximations produced from a probabilistic counter, so they may differ slightly
from the exact number of pages touched. `Pages marked for reallocation` counts the pages that
qualified, not the segments that were actually moved, since a segment that was in use at the time
is skipped even though its page was marked.

The `defrag_attempt_total` and `defrag_realloc_total` fields of [`INFO`](./info.md) track the
value-level defragmentation task only, and are not advanced by this command.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `threshold` is not a valid
floating point number, is outside the accepted range, or if an extra argument is supplied.

## Examples

The database below holds 400,000 keys and shares its pages with a second database that has since
been flushed. [`MEMORY ARENA SUMMARY`](./memory-arena.md) shows the effect: the block size that
backs the segments is committing 21 MB to hold 18 MB of live segments, wasting 12.65% of it.

```shell
dragonfly> DBSIZE
(integer) 400000

dragonfly> INFO memory
# Memory
used_memory:31436960
used_memory_rss:53485568
...

dragonfly> MEMORY ARENA SUMMARY
...
Arena statistics for machine:
 BlockSize   Reserved  Committed       Used     Wasted   Waste%
        64     130688       8192        128       8064    98.44%
         8     131008       8192         32       8160    99.61%
      1792     127232      14336       3584      10752    75.00%
      4096     131072      32768       8192      24576    75.00%
     20480    1003520     163840      81920      81920    50.00%
        32   13938720   13938720   12800000    1138720     8.17%
     32768   21495808   21233664   18546688    2686976    12.65%
    Total:   36958048   35399712   31440544    3959168    11.18%
```

The first invocation finds three pages worth consolidating:

```shell
dragonfly> MEMORY DEFRAGMENT-SEGMENTS
Page usage threshold: 80
Pages scanned: 23
Pages marked for reallocation: 3
Pages full: 20
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
```

Repeating it walks the rest of the table and then settles at zero, which is the signal to stop:

```shell
run 2:  Pages marked for reallocation: 5
run 3:  Pages marked for reallocation: 5
run 4:  Pages marked for reallocation: 6
run 5:  Pages marked for reallocation: 3
run 6:  Pages marked for reallocation: 2
run 7:  Pages marked for reallocation: 1
run 8:  Pages marked for reallocation: 0
```

The waste in the segment block size has dropped from 12.65% to 1.74%, and the freed pages have left
the resident set:

```shell
dragonfly> INFO memory
# Memory
used_memory:31436960
used_memory_rss:51863552
...

dragonfly> MEMORY ARENA SUMMARY
...
Arena statistics for machine:
 BlockSize   Reserved  Committed       Used     Wasted   Waste%
        64     130688       8192        128       8064    98.44%
         8     131008       8192         32       8160    99.61%
      1792     127232      14336       3584      10752    75.00%
      4096     131072      32768       8192      24576    75.00%
     20480    1003520     163840      81920      81920    50.00%
     32768   18874368   18874368   18546688     327680     1.74%
        32   13938720   13938720   12800000    1138720     8.17%
    Total:   34336608   33040416   31440544    1599872     4.84%
```

Note that `used_memory` is unchanged throughout: defragmentation moves live data rather than
freeing it, so only the resident set shrinks.

Once the table is consolidated, a stricter threshold finds nothing to do — every page holding a
segment is now full:

```shell
dragonfly> MEMORY DEFRAGMENT-SEGMENTS 0.5
Page usage threshold: 50
Pages scanned: 36
Pages marked for reallocation: 0
Pages full: 34
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

Because the command is scoped to the selected database, running it on a database that holds no data
reports only the pages backing the empty table:

```shell
dragonfly> SELECT 3
OK
dragonfly> MEMORY DEFRAGMENT-SEGMENTS
Page usage threshold: 80
Pages scanned: 4
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

Invalid arguments:

```shell
dragonfly> MEMORY DEFRAGMENT-SEGMENTS abc
(error) ERR value is not a valid float

dragonfly> MEMORY DEFRAGMENT-SEGMENTS 2
(error) ERR Threshold must be between 0 and 1

dragonfly> MEMORY DEFRAGMENT-SEGMENTS 0
(error) ERR Threshold must be between 0 and 1

dragonfly> MEMORY DEFRAGMENT-SEGMENTS 0.9 xyz
(error) ERR syntax error
```

## See also

[`MEMORY`](./memory.md) | [`MEMORY DEFRAGMENT`](./memory-defragment.md) | [`MEMORY DECOMMIT`](./memory-decommit.md) | [`MEMORY ARENA`](./memory-arena.md) | [`MEMORY HELP`](./memory-help.md) | [Server configuration flags](../../managing-dragonfly/flags.md)
