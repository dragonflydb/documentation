---
description: Learn how to use Dragonfly's MEMORY DEFRAGMENT command to reclaim fragmented memory.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY DEFRAGMENT

<PageTitle title="Dragonfly MEMORY DEFRAGMENT Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY DEFRAGMENT [threshold]

**Time complexity:** Depends on the number of database entries examined.

**ACL categories:** @read, @slow

`MEMORY DEFRAGMENT` attempts to reclaim fragmented memory by moving allocations
out of sparsely used pages. It waits for the defragmentation pass to run on all
shards, so it can take time on a large dataset.

The optional `threshold` is a page-utilization fraction. Pages whose utilization
is below the threshold are candidates for moving their data. When omitted,
Dragonfly uses the `--mem_defrag_page_utilization_threshold` setting (default:
`0.8`, or 80% utilization).

## Return

A report describing the pages scanned and marked for reallocation.

## Examples

```shell
dragonfly> MEMORY DEFRAGMENT 0.8
```
