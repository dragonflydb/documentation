---
description: Learn how to use the TOPK.COUNT command to get estimated counts of items in a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.COUNT

<PageTitle title="Redis TOPK.COUNT Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.COUNT key item [item ...]

**Time complexity:** O(n) where n is the number of items

**ACL categories:** @topk

Returns an approximate per-item count from the internal Count-Min Sketch backing
the Top-K structure. The `key` must already exist (created via
[`TOPK.RESERVE`](./topk.reserve.md)); otherwise an error is returned.

**Important:** in Dragonfly the value returned by `TOPK.COUNT` is the residual
counter inside the sketch — not the total number of times an item was added.
For items currently held by the Top-K min-heap the counter is usually `0`. The
counter only grows for items that hashed into a bucket but were beaten by a
stronger item, so the meaning is closer to "approximate excess insertions" than
"frequency".

To check whether an item is currently in the Top-K list, use
[`TOPK.QUERY`](./topk.query.md). To see the actual items and the counts the
heap keeps for them, use [`TOPK.LIST WITHCOUNT`](./topk.list.md).

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array of integers,
one per queried item, containing the sketch-side counter for that item (often
`0` for items currently in the Top-K list).

## Examples

Track page views with a small Top-K, then compare the three observation commands:

```shell
dragonfly> TOPK.RESERVE pageviews 2 200 6 0.9
OK
dragonfly> TOPK.ADD pageviews /home /home /home /pricing /pricing /about /docs
1) (nil)
2) (nil)
3) (nil)
4) (nil)
5) (nil)
6) (nil)
7) (nil)
dragonfly> TOPK.LIST pageviews
1) "/about"
2) "/home"
dragonfly> TOPK.QUERY pageviews /home /pricing /about /docs /signup
1) (integer) 1
2) (integer) 0
3) (integer) 1
4) (integer) 0
5) (integer) 0
dragonfly> TOPK.COUNT pageviews /home /pricing /about /docs /signup
1) (integer) 1
2) (integer) 0
3) (integer) 1
4) (integer) 1
5) (integer) 0
```

`TOPK.QUERY` answers the natural question "is this item in the Top-K right
now?" The exact membership of the Top-K min-heap is sensitive to the chosen
`width`, `depth`, and `decay` parameters — different parameters can keep
different items.

`TOPK.COUNT` returns the residual sketch counter, which behaves differently
from a frequency estimate. Above, `/docs` was added once and immediately
displaced, so its counter is `1`. `/signup` was never added, so its counter
is `0`. For items currently in the Top-K the value is dominated by how the
sketch hashed them rather than by their total arrival count, so do not rely
on `TOPK.COUNT` for frequency statistics — use [`TOPK.LIST
WITHCOUNT`](./topk.list.md) instead.
## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.QUERY`](./topk.query.md) | [`TOPK.LIST`](./topk.list.md) | [`TOPK.INFO`](./topk.info.md)
