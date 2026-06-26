---
description: Learn how to use the CF.ADDNX command to add an item to a Cuckoo filter only if it does not already exist.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.ADDNX

<PageTitle title="Redis CF.ADDNX Command (Documentation) | Dragonfly" />

## Syntax

    CF.ADDNX key item

**Time complexity:** O(k + i), where k is the number of sub-filters and i is `MAXITERATIONS`

**ACL categories:** @cuckoo

Adds a single `item` to the Cuckoo filter at `key` only if it does not already exist.
If `key` does not exist, a new filter is created with default parameters.

Unlike [`CF.ADD`](./cf.add.md), this command checks for the item before inserting.
Because Cuckoo filters can return false positives, `CF.ADDNX` may decline to insert
an item that was never actually added.

If the filter is full and expansion is disabled (`EXPANSION 0`), an error is returned.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers):

- `1` if the item was successfully added.
- `0` if the item already exists in the filter (or is a false positive match).

## Examples

```shell
dragonfly> CF.ADDNX cf Hello
(integer) 1

dragonfly> CF.ADDNX cf Hello
(integer) 0

dragonfly> CF.ADDNX cf World
(integer) 1
```

## See also

[`CF.ADD`](./cf.add.md) | [`CF.RESERVE`](./cf.reserve.md)
