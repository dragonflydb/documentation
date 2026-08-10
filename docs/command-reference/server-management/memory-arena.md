---
description:  Learn how to use the Dragonfly MEMORY ARENA command to inspect per-thread allocator arena statistics.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY ARENA

<PageTitle title="Dragonfly MEMORY ARENA Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY ARENA [SUMMARY] [BACKING] [thread-id]
    MEMORY ARENA SHOW

**Time complexity:** O(N) where N is the number of heap pages inspected.

**ACL categories:** @read, @slow

The `MEMORY ARENA` command reports allocator arena statistics broken down by block size. It is a
diagnostic command, useful for understanding where committed memory is going and how much of it is
wasted on partially filled blocks. This command is Dragonfly-specific.

Because Dragonfly is multi-threaded and each thread allocates from its own heap, the statistics are
per thread. By default the command reports the heap of thread `0`; pass a `thread-id` to inspect a
different thread.

## Options

**`SUMMARY`** reports every thread in turn, followed by a machine-wide total, with the rows
aggregated by block size. A `thread-id` cannot be combined with `SUMMARY`, since the summary
already covers all threads.

**`BACKING`** reports the backing heap — the heap used for the server's own bookkeeping
allocations — instead of the heap that holds user data.

**`SHOW`** prints a process-wide arena report to the server's standard output and replies `OK`. The
report does not come back over the connection, and the server must have been started with the
`MIMALLOC_VERBOSE=1` environment variable for anything to be printed. `SHOW` takes no further
arguments.

## Return

[Verbatim string reply](https://valkey.io/topics/protocol/#verbatim-strings): the arena statistics
report, for every form except `SHOW`.

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` for `MEMORY ARENA SHOW`.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `thread-id` is not less than
the number of threads, or if an argument follows `SUMMARY` or `SHOW`.

The default report has one row per block size, with the following columns.

| Column | Description |
| --- | --- |
| `Count` | Number of heap pages holding blocks of this size. |
| `BlockSize` | Size in bytes of each block in the row. |
| `Reserved` | Address space reserved for those pages. |
| `Committed` | Memory actually committed and backed by the operating system. |
| `Used` | Memory occupied by live allocations. |

The `SUMMARY` form replaces `Count` with two derived columns: `Wasted`, the difference between
committed and used memory, and `Waste%`, the same figure as a percentage of committed memory.

## Examples

The default form reports one thread, ending with a process-level fragmentation figure:

```shell
dragonfly> MEMORY ARENA

Arena statistics from thread:0
Count BlockSize Reserved Committed Used
1 20480 512000 81920 20480
1 32 65440 4096 96
1 8 65504 4096 32
1 16 65488 4096 0
1 32768 524288 262144 262144
1 1792 62720 7168 1792
1 64 65344 4096 128
total reserved: 1360784, committed: 367616, used: 284672 fragmentation waste: 22.5627%
--- End mimalloc statistics, took 7us ---
```

`SUMMARY` sorts the same data by block size and adds the waste columns, one table per thread
followed by a machine-wide table:

```shell
dragonfly> MEMORY ARENA SUMMARY

Arena statistics for thread 0:
 BlockSize   Reserved  Committed       Used     Wasted   Waste%
     32768     524288     262144     262144          0     0.00%
        64      65344       4096        128       3968    96.88%
        32      65440       4096         96       4000    97.66%
         8      65504       4096         32       4064    99.22%
        16      65488       4096          0       4096   100.00%
      1792      62720       7168       1792       5376    75.00%
     20480     512000      81920      20480      61440    75.00%
    Total:    1360784     367616     284672      82944    22.56%

Arena statistics for thread 1:
 BlockSize   Reserved  Committed       Used     Wasted   Waste%
     32768     524288     262144     262144          0     0.00%
      1792      64512       7168       3584       3584    50.00%
        64      65344       4096         64       4032    98.44%
        32      65440       4096         32       4064    99.22%
         8      65504       4096          8       4088    99.80%
        16      65488       4096          0       4096   100.00%
     20480     491520      81920      20480      61440    75.00%
    Total:    1342096     367616     286312      81304    22.12%

Arena statistics for machine:
 BlockSize   Reserved  Committed       Used     Wasted   Waste%
     32768    1048576     524288     524288          0     0.00%
        64     130688       8192        192       8000    97.66%
        32     130880       8192        128       8064    98.44%
         8     131008       8192         40       8152    99.51%
        16     130976       8192          0       8192   100.00%
      1792     127232      14336       5376       8960    62.50%
     20480    1003520     163840      40960     122880    75.00%
    Total:    2702880     735232     570984     164248    22.34%

--- End mimalloc statistics, took 38us ---
```

Requesting a thread that does not exist is an error, as is passing a thread id together with
`SUMMARY`:

```shell
dragonfly> MEMORY ARENA 99
(error) ERR Thread id must be less than 2

dragonfly> MEMORY ARENA SUMMARY 0
(error) ERR syntax error
```

## See also

[`MEMORY`](./memory.md) | [`MEMORY MALLOC-STATS`](./memory-malloc-stats.md) | [`MEMORY DECOMMIT`](./memory-decommit.md) | [`MEMORY DEFRAGMENT`](./memory-defragment.md)
