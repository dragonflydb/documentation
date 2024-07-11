---
description: Learn how to use Redis BF.EXISTS command to check for the existence of an item in the Bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.EXISTS

<PageTitle title="Redis BF.EXISTS Command (Documentation) | Dragonfly" />

## Syntax

    BF.EXISTS key item

**Time complexity:** O(1)

**ACL categories:** @bloom

Checks for the existence of a single item in a Bloom filter `key`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers):

- `1` if the item exists with a high probability.
- `0` if the item definitely does not exist.

## Examples

```shell
dragonfly> BF.ADD bf Hello
(integer) 1

dragonfly> BF.EXISTS bf Hello
(integer) 1

dragonfly> BF.EXISTS bf World
(integer) 0
```

## See also

[`BF.ADD`](./bf.add.md) | [`BF.MEXISTS`](./bf.mexists.md)
