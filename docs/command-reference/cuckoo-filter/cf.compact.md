---
description: Learn how to use the CF.COMPACT command to compact a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.COMPACT

<PageTitle title="CF.COMPACT Command (Documentation) | Dragonfly" />

## Syntax

    CF.COMPACT key

**Time complexity:** O(k), where k is the number of sub-filters

**ACL categories:** @cuckoo

Attempts to compact the Cuckoo filter at `key` by consolidating its sub-filters.

When a filter expands, older sub-filters are kept around until [`CF.DEL`](./cf.del.md) empties
them out. `CF.DEL` already triggers this automatically once deletions exceed 10% of the items in
the filter, so `CF.COMPACT` mainly exists to force the pass on demand, for example after a batch
of deletions.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` does not exist or is not a Cuckoo filter.

## Examples

```shell
dragonfly> CF.RESERVE cf 4
OK

dragonfly> CF.ADD cf Hello
(integer) 1

dragonfly> CF.DEL cf Hello
(integer) 1

dragonfly> CF.COMPACT cf
OK

dragonfly> CF.COMPACT no_such_key
(error) no such key
```

## See also

[`CF.DEL`](./cf.del.md) | [`CF.RESERVE`](./cf.reserve.md) | [`CF.INFO`](./cf.info.md)
