---
description: Learn how to use the CF.COUNT command to count occurrences of an item in a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.COUNT

<PageTitle title="Redis CF.COUNT Command (Documentation) | Dragonfly" />

## Syntax

    CF.COUNT key item

**Time complexity:** O(k), where k is the number of sub-filters

**ACL categories:** @cuckoo

Returns the number of times `item` occurs in the Cuckoo filter at `key`.

Since [`CF.ADD`](./cf.add.md) allows duplicate insertions, the same item can occupy more than one
slot. `CF.COUNT` reports how many slots currently match `item`, which may include false positives.

If `key` does not exist, `0` is returned.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): the number of occurrences of `item` in the filter.

## Examples

```shell
dragonfly> CF.ADD cf foo
(integer) 1

dragonfly> CF.ADD cf foo
(integer) 1

dragonfly> CF.COUNT cf foo
(integer) 2

dragonfly> CF.COUNT cf bar
(integer) 0

dragonfly> CF.COUNT no_such_key foo
(integer) 0
```

## See also

[`CF.ADD`](./cf.add.md) | [`CF.EXISTS`](./cf.exists.md) | [`CF.DEL`](./cf.del.md)
