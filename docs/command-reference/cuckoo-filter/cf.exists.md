---
description: Learn how to use the CF.EXISTS command to check if an item exists in a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.EXISTS

<PageTitle title="Redis CF.EXISTS Command (Documentation) | Dragonfly" />

## Syntax

    CF.EXISTS key item

**Time complexity:** O(k), where k is the number of sub-filters

**ACL categories:** @cuckoo

Checks whether `item` exists in the Cuckoo filter at `key`.

Cuckoo filters may return false positives — an item that was never inserted may
still be reported as present due to a fingerprint collision. False negatives are
not possible: if an item was inserted and never deleted, `CF.EXISTS` will always
return `1`.

If `key` does not exist, `0` is returned.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers):

- `1` if the item exists (or is a false positive match).
- `0` if the item does not exist.

## Examples

```shell
dragonfly> CF.ADD cf Hello
(integer) 1

dragonfly> CF.EXISTS cf Hello
(integer) 1

dragonfly> CF.EXISTS cf World
(integer) 0

dragonfly> CF.EXISTS no_such_key item
(integer) 0
```

## See also

[`CF.MEXISTS`](./cf.mexists.md) | [`CF.ADD`](./cf.add.md) | [`CF.RESERVE`](./cf.reserve.md)
