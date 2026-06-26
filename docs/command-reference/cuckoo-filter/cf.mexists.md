---
description: Learn how to use the CF.MEXISTS command to check multiple items in a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.MEXISTS

<PageTitle title="Redis CF.MEXISTS Command (Documentation) | Dragonfly" />

## Syntax

    CF.MEXISTS key item [item ...]

**Time complexity:** O(k * n), where k is the number of sub-filters and n is the number of items

**ACL categories:** @cuckoo

Checks whether one or more items exist in the Cuckoo filter at `key`.
Returns one reply per item in the same order as the input.

Like [`CF.EXISTS`](./cf.exists.md), false positives are possible but false negatives are not.
If `key` does not exist, `0` is returned for every item.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays) of [Integer replies](https://valkey.io/topics/protocol/#integers), one per item:

- `1` if the item exists (or is a false positive match).
- `0` if the item does not exist.

## Examples

```shell
dragonfly> CF.ADD cf Hello
(integer) 1

dragonfly> CF.ADD cf World
(integer) 1

dragonfly> CF.MEXISTS cf Hello World Missing
1) (integer) 1
2) (integer) 1
3) (integer) 0

dragonfly> CF.MEXISTS no_such_key a b c
1) (integer) 0
2) (integer) 0
3) (integer) 0
```

## See also

[`CF.EXISTS`](./cf.exists.md) | [`CF.ADD`](./cf.add.md) | [`CF.RESERVE`](./cf.reserve.md)
