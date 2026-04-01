---
description: Learn how to use the TOPK.ADD command to add items to a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.ADD

<PageTitle title="Redis TOPK.ADD Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.ADD key item [item ...]

**Time complexity:** O(n * depth) where n is the number of items

**ACL categories:** @topk

Adds one or more items to the Top-K data structure stored at `key`.
The `key` must already exist (created via [`TOPK.RESERVE`](./topk.reserve.md)); otherwise, an error is returned.
If an added item displaces an existing item from the top-k list, the displaced item is returned.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array with one entry per item.
Each entry is either:

- A bulk string with the name of the item that was displaced from the top-k list.
- `nil` if no item was displaced.

## Examples

```shell
dragonfly> TOPK.RESERVE topk 2
OK

dragonfly> TOPK.ADD topk foo bar baz
1) (nil)
2) (nil)
3) foo

dragonfly> TOPK.LIST topk
1) baz
2) bar
```

## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.INCRBY`](./topk.incrby.md) | [`TOPK.QUERY`](./topk.query.md) | [`TOPK.LIST`](./topk.list.md)
