---
description: Learn how to use the TOPK.LIST command to list all items in a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.LIST

<PageTitle title="Redis TOPK.LIST Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.LIST key [WITHCOUNT]

**Time complexity:** O(k log k) where k is the number of top items tracked

**ACL categories:** @topk

Returns all items currently tracked in the Top-K data structure stored at `key`, sorted by estimated count in descending order.
The `key` must already exist (created via [`TOPK.RESERVE`](./topk.reserve.md)); otherwise, an error is returned.
If no items have been added yet, an empty array is returned.
If the optional `WITHCOUNT` flag is specified, the estimated count of each item is also returned.

## Return

Without `WITHCOUNT`:
[Array reply](https://valkey.io/topics/protocol/#arrays): An array of bulk strings representing the items in the top-k list.

With `WITHCOUNT`:
[Array reply](https://valkey.io/topics/protocol/#arrays): A flat array of item-count pairs, where each item name is followed by its estimated count.

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

dragonfly> TOPK.LIST topk
1) foo
2) bar
3) baz

dragonfly> TOPK.LIST topk WITHCOUNT
1) foo
2) (integer) 3
3) bar
4) (integer) 2
5) baz
6) (integer) 1
```

## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.ADD`](./topk.add.md) | [`TOPK.QUERY`](./topk.query.md) | [`TOPK.INFO`](./topk.info.md)
