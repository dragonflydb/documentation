---
description: Learn how to use Redis BF.ADD command to add an item to the Bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.ADD

<PageTitle title="Redis BF.ADD Command (Documentation) | Dragonfly" />

## Syntax

    BF.ADD key item

**Time complexity:** O(1)

**ACL categories:** @bloom

Adds a single item to a Bloom filter `key`.
If the `key` does not exist, a new Bloom filter is created with default parameters.

## Returns

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers):

- `1` if the item was successfully added to the filter.
- `0` if the item was already added to the filter, which could be a false positive.

## Examples

```shell
dragonfly> BF.ADD bf "Hello"
(integer) 1

dragonfly> BF.ADD bf "Hello"
(integer) 0
```

## See also

[`BF.RESERVE`](./bf.reserve.md) | [`BF.MADD`](./bf.madd.md)
