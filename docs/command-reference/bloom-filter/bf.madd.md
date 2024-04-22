---
description: Learn how to use Redis BF.MADD command to add one or more items to the Bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.MADD

<PageTitle title="Redis BF.MADD Command (Documentation) | Dragonfly" />

## Syntax

    BF.MADD key item [item ...]

**Time complexity:** O(1) for each item added, so O(N) to add N items when the command is called with multiple arguments.

**ACL categories:** @bloom

Adds one or more items to a Bloom filter `key`.

## Returns

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays):
an array of integers, each representing the result for an individual item as if being processed by the [`BF.ADD`](./bf.add.md) command:

- `1` if the item was successfully added to the filter.
- `0` if the item was already added to the filter, which could be a false positive.

## Examples

```shell
dragonfly> BF.MADD bf Hello World
1) (integer) 1
2) (integer) 1
```

## See also

[`BF.RESERVE`](./bf.reserve.md) | [`BF.ADD`](./bf.add.md)
