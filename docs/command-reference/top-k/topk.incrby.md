---
description: Learn how to use the TOPK.INCRBY command to increment item counts in a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.INCRBY

<PageTitle title="Redis TOPK.INCRBY Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.INCRBY key item increment [item increment ...]

**Time complexity:** O(n * depth) where n is the number of items

**ACL categories:** @topk

Increments the count of one or more items in the Top-K data structure stored at `key` by the given `increment` values.
The `key` must already exist (created via [`TOPK.RESERVE`](./topk.reserve.md)); otherwise, an error is returned.
The `increment` value must be a positive integer between `1` and `100000`.
If an item displaces an existing item from the top-k list, the displaced item is returned.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array with one entry per item.
Each entry is either:

- A bulk string with the name of the item that was displaced from the top-k list.
- `nil` if no item was displaced.

## Examples

```shell
dragonfly> TOPK.RESERVE topk 2
OK

dragonfly> TOPK.INCRBY topk foo 3 bar 5 baz 10
1) (nil)
2) (nil)
3) foo

dragonfly> TOPK.LIST topk WITHCOUNT
1) baz
2) (integer) 10
3) bar
4) (integer) 5
```

## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.ADD`](./topk.add.md) | [`TOPK.COUNT`](./topk.count.md) | [`TOPK.LIST`](./topk.list.md)
