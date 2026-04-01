---
description: Learn how to use the TOPK.COUNT command to get estimated counts of items in a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.COUNT

<PageTitle title="Redis TOPK.COUNT Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.COUNT key item [item ...]

**Time complexity:** O(n * depth) where n is the number of items and depth is the number of hash function rows

**ACL categories:** @topk

Returns the estimated count of one or more items in the Top-K data structure stored at `key`.
The `key` must already exist (created via [`TOPK.RESERVE`](./topk.reserve.md)); otherwise, an error is returned.
The returned counts are estimates and may differ from the true counts due to the probabilistic nature of the underlying Count-Min Sketch.
An item can have a non-zero estimated count even if it is not currently in the top-k list (as reported by [`TOPK.QUERY`](./topk.query.md)).

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array of integers, one per item, representing the estimated count of each queried item.

## Examples

```shell
dragonfly> TOPK.RESERVE topk 3
OK

dragonfly> TOPK.ADD topk foo foo foo bar bar baz
1) (nil)
2) (nil)
3) (nil)
4) (nil)
5) (nil)
6) (nil)

dragonfly> TOPK.COUNT topk foo bar baz
1) (integer) 3
2) (integer) 2
3) (integer) 1
```

## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.QUERY`](./topk.query.md) | [`TOPK.LIST`](./topk.list.md) | [`TOPK.INFO`](./topk.info.md)
