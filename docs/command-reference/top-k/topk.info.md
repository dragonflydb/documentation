---
description: Learn how to use the TOPK.INFO command to retrieve information about a Top-K data structure in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# TOPK.INFO

<PageTitle title="Redis TOPK.INFO Command (Documentation) | Dragonfly" />

## Syntax

    TOPK.INFO key

**Time complexity:** O(1)

**ACL categories:** @topk

Returns metadata about the Top-K data structure stored at `key`, including its configuration parameters.
The `key` must already exist (created via [`TOPK.RESERVE`](./topk.reserve.md)); otherwise, an error is returned.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): A flat array of field-value pairs with the following fields:

- `k`: The number of top items tracked.
- `width`: The number of counters per hash function row.
- `depth`: The number of hash function rows.
- `decay`: The probability decay factor.

## Examples

```shell
dragonfly> TOPK.RESERVE topk 5 20 7 0.9
OK

dragonfly> TOPK.INFO topk
1) k
2) (integer) 5
3) width
4) (integer) 20
5) depth
6) (integer) 7
7) decay
8) "0.9"
```

## See also

[`TOPK.RESERVE`](./topk.reserve.md) | [`TOPK.LIST`](./topk.list.md) | [`TOPK.COUNT`](./topk.count.md)
