---
description: Learn how to use the CF.ADD command to add an item to a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.ADD

<PageTitle title="CF.ADD Command (Documentation) | Dragonfly" />

## Syntax

    CF.ADD key item

**Time complexity:** O(k + i), where k is the number of sub-filters and i is `MAXITERATIONS`

**ACL categories:** @cuckoo

Adds a single `item` to the Cuckoo filter at `key`.
If `key` does not exist, a new filter is created with default parameters.

Unlike [`CF.ADDNX`](./cf.addnx.md), duplicate insertions are allowed — the same item can be added multiple times and will occupy a separate slot each time.
Use `CF.DEL` once per insertion to remove it.

If the filter is full and expansion is disabled (`EXPANSION 0`), an error is returned.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers):

- `1` if the item was successfully added.

If the filter is full and cannot be expanded, an error is returned instead of an integer reply.

## Examples

```shell
dragonfly> CF.ADD cf Hello
(integer) 1

dragonfly> CF.ADD cf Hello
(integer) 1

dragonfly> CF.COUNT cf Hello
(integer) 2
```

## See also

[`CF.ADDNX`](./cf.addnx.md) | [`CF.INSERT`](./cf.insert.md) | [`CF.EXISTS`](./cf.exists.md) | [`CF.RESERVE`](./cf.reserve.md)
