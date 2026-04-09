---
description: Learn how to use the TOPK.QUERY command to check if items are in the Top-K list in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.QUERY

<PageTitle title="Redis TOPK.QUERY Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.QUERY key item [item ...]

**Time complexity:** O(k) per queried item, or O(m * k) when querying m items at once

**ACL categories:** @topk

Checks whether one or more items are currently in the Top-K list stored at `key`.
The `key` must already exist (created via [`TOPK.RESERVE`](./topk.reserve.md)); otherwise, an error is returned.
Each item is checked via a linear scan of the top-k heap.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array of integers, one per item:

- `1` if the item is in the top-k list.
- `0` if the item is not in the top-k list.

## Examples

```shell
dragonfly> TOPK.RESERVE topk 2
OK

dragonfly> TOPK.ADD topk foo bar baz
1) (nil)
2) (nil)
3) foo

dragonfly> TOPK.QUERY topk foo bar baz
1) (integer) 0
2) (integer) 1
3) (integer) 1
```

## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.ADD`](./topk.add.md) | [`TOPK.COUNT`](./topk.count.md) | [`TOPK.LIST`](./topk.list.md)
