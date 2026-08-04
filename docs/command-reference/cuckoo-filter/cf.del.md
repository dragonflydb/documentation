---
description: Learn how to use the CF.DEL command to remove an item from a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.DEL

<PageTitle title="CF.DEL Command (Documentation) | Dragonfly" />

## Syntax

    CF.DEL key item

**Time complexity:** O(k), where k is the number of sub-filters

**ACL categories:** @cuckoo

Removes a single occurrence of `item` from the Cuckoo filter at `key`.

Unlike Bloom filters, Cuckoo filters support deletion. Only one occurrence is removed per call,
so if `item` was added multiple times, `CF.DEL` must be called once per insertion to fully remove it.

Deleting an item that was never added, or deleting more times than it was added, can introduce
false negatives for that item. Only delete items that are known to have been added.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers):

- `1` if the item was found and removed.
- `0` if the item was not found.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` does not exist or is not a Cuckoo filter.

## Examples

```shell
dragonfly> CF.ADD cf Hello
(integer) 1

dragonfly> CF.DEL cf Hello
(integer) 1

dragonfly> CF.EXISTS cf Hello
(integer) 0

dragonfly> CF.DEL cf Hello
(integer) 0

dragonfly> CF.DEL no_such_key Hello
(error) no such key
```

## See also

[`CF.ADD`](./cf.add.md) | [`CF.COUNT`](./cf.count.md) | [`CF.COMPACT`](./cf.compact.md)
