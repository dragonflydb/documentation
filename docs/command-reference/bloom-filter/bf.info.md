---
description: Learn how to use Redis BF.INFO to inspect a Bloom filter in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# BF.INFO

<PageTitle title="Redis BF.INFO Command (Documentation) | Dragonfly" />

## Syntax

    BF.INFO key [CAPACITY | SIZE | FILTERS | ITEMS | EXPANSION]

**Time complexity:** O(F), where F is the number of sub-filters.

**ACL categories:** @bloom

Returns usage information and properties of the Bloom filter stored at `key`.
Without a selector, the command returns all available properties. With a
selector, it returns only that property's value.

## Selectors

| Selector | Description |
|---|---|
| `CAPACITY` | Total design capacity across completed sub-filters and the current sub-filter. The value can be greater than the capacity requested with `BF.RESERVE` because Dragonfly rounds the underlying storage size. |
| `SIZE` | Number of bytes allocated by the filter. |
| `FILTERS` | Number of sub-filters. |
| `ITEMS` | Number of items successfully inserted across all sub-filters. |
| `EXPANSION` | Growth factor used when another sub-filter is created. |

:::note Dragonfly compatibility

Dragonfly v1.40.0 supports the five selectors listed above. The `ERROR`,
`TIGHTENING`, and `MAXSCALEDCAPACITY` selectors from the
[Valkey command](https://valkey.io/commands/bf.info/) are not supported.

:::

## Return

- [Array reply](https://valkey.io/topics/protocol/#arrays): alternating property
  names and integer values when no selector is provided.
- [Integer reply](https://valkey.io/topics/protocol/#integers): the requested
  property value when a selector is provided.
- [Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` does
  not exist, contains a different data type, or the selector is unsupported.

## Examples

```shell
dragonfly> BF.RESERVE visitors 0.01 1000
OK

dragonfly> BF.MADD visitors alice bob carol
1) (integer) 1
2) (integer) 1
3) (integer) 1

dragonfly> BF.INFO visitors
 1) "Capacity"
 2) (integer) 1485
 3) "Size"
 4) (integer) 2136
 5) "Number of filters"
 6) (integer) 1
 7) "Number of items inserted"
 8) (integer) 3
 9) "Expansion rate"
10) (integer) 2

dragonfly> BF.INFO visitors ITEMS
(integer) 3
```

## See also

[`BF.RESERVE`](./bf.reserve.md) | [`BF.ADD`](./bf.add.md) | [`BF.MADD`](./bf.madd.md)
