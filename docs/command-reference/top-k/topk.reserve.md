---
description: Learn how to use the TOPK.RESERVE command to initialize a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.RESERVE

<PageTitle title="Redis TOPK.RESERVE Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.RESERVE key topk [width depth decay]

**Time complexity:** O(1)

**ACL categories:** @topk

Creates a new Top-K data structure at `key` that tracks the top `topk` most frequent items.

- `topk`: The number of top items to track (between `1` and `100000`).
- `width` (optional): The number of counters per hash function row (default `8`, max `1000000`).
- `depth` (optional): The number of hash function rows (default `7`, max `100`).
- `decay` (optional): The probability decay factor between `0` and `1` (default `0.9`).

If `width`, `depth`, and `decay` are provided, all three must be specified together.
If `key` already exists, an error (`item exists`) is returned.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the Top-K was created successfully.

An error is returned if:
- The `key` already exists.
- The parameters are out of the allowed ranges.

## Examples

```shell
dragonfly> TOPK.RESERVE topk 3
OK

dragonfly> TOPK.RESERVE topk_custom 5 20 7 0.9
OK
```

## See also

[`TOPK.ADD`](./topk.add.md) | [`TOPK.INFO`](./topk.info.md) | [`TOPK.LIST`](./topk.list.md)
