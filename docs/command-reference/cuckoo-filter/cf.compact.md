---
description: Learn how to use the CF.COMPACT command to compact a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.COMPACT

<PageTitle title="CF.COMPACT Command (Documentation) | Dragonfly" />

## Syntax

    CF.COMPACT key

**Time complexity:** O(S × k) in the worst case, where S is the total number of fingerprint slots and k is the number of sub-filters.

**ACL categories:** @cuckoo_filter, @slow, @write

Attempts to compact the Cuckoo filter at `key` by consolidating its sub-filters.

Compaction scans newer sub-filters and tries to move their fingerprints into
free slots in older sub-filters. It can remove a sub-filter only when the newest
one becomes completely empty.

[`CF.DEL`](./cf.del.md) automatically runs a compaction pass when accumulated
deletions exceed one tenth of the remaining items. `CF.COMPACT` forces a full
pass on demand, for example after a batch of deletions.

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
(error) ERR no such key
```

## See also

[`CF.DEL`](./cf.del.md) | [`CF.RESERVE`](./cf.reserve.md) | [`CF.INFO`](./cf.info.md)
