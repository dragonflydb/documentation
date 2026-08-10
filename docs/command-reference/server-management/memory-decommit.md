---
description:  Learn how to use the Dragonfly MEMORY DECOMMIT command to return freed memory back to the operating system.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY DECOMMIT

<PageTitle title="Dragonfly MEMORY DECOMMIT Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY DECOMMIT [COOL]

**Time complexity:** O(N) where N is the number of heap pages inspected.

**ACL categories:** @read, @slow

The `MEMORY DECOMMIT` command asks the allocator to return memory that the server has already
freed back to the operating system, which lowers the process resident set size reported as
`used_memory_rss` by [`INFO`](./info.md). This command is Dragonfly-specific.

Freeing data inside Dragonfly does not immediately shrink the process: the allocator keeps the
underlying pages so it can reuse them without going back to the kernel. `MEMORY DECOMMIT` forces
that memory to be given up now. It only affects pages that are already fully free — to first
consolidate live objects scattered across partially used pages, run
[`MEMORY DEFRAGMENT`](./memory-defragment.md) before it.

Redis's `MEMORY PURGE` is not implemented in Dragonfly; `MEMORY DECOMMIT` serves the same purpose.

## The COOL option

`COOL` selects a different operation rather than extending the default one. Instead of decommitting
memory, it flushes the cool queue of [tiered storage](../../managing-dragonfly/tiering.md) to disk:
values that have been offloaded but whose in-memory copy is still cached are written out and their
memory released.

`MEMORY DECOMMIT COOL` therefore does not decommit; issue `MEMORY DECOMMIT` separately if both are
wanted.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if any argument other than `COOL`
is given.

## Examples

```shell
dragonfly> INFO memory
# Memory
used_memory_rss:32104448
...

dragonfly> MEMORY DECOMMIT
OK

dragonfly> INFO memory
# Memory
used_memory_rss:31899648
...

dragonfly> MEMORY DECOMMIT COOL
OK

dragonfly> MEMORY DECOMMIT XYZ
(error) ERR syntax error
```

## See also

[`MEMORY`](./memory.md) | [`MEMORY DEFRAGMENT`](./memory-defragment.md) | [`MEMORY ARENA`](./memory-arena.md) | [`INFO`](./info.md)
