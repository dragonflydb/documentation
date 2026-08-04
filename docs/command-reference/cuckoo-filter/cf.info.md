---
description: Learn how to use the CF.INFO command to get information about a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.INFO

<PageTitle title="CF.INFO Command (Documentation) | Dragonfly" />

## Syntax

    CF.INFO key

**Time complexity:** O(k), where k is the number of sub-filters.

**ACL categories:** @cuckoo_filter, @fast, @read

Returns information about the Cuckoo filter at `key`.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays) of alternating field names and values:

- `Size`: memory used by the filter, in bytes.
- `Number of buckets`: configured base number of buckets in the initial sub-filter.
- `Number of filters`: total number of sub-filters, including the initial one.
- `Number of items inserted`: total number of items currently in the filter.
- `Number of items deleted`: number of deletions accumulated since the last compaction.
- `Bucket size`: number of fingerprint slots per bucket.
- `Expansion rate`: effective expansion rate after rounding a nonzero configured value up to the next power of two.
- `Max iterations`: the configured maximum number of cuckoo-displacement attempts.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` does not exist or is not a Cuckoo filter.

## Examples

```shell
dragonfly> CF.RESERVE cf 1000 BUCKETSIZE 4 MAXITERATIONS 10 EXPANSION 2
OK

dragonfly> CF.ADD cf foo
(integer) 1

dragonfly> CF.INFO cf
 1) "Size"
 2) (integer) 1136
 3) "Number of buckets"
 4) (integer) 256
 5) "Number of filters"
 6) (integer) 1
 7) "Number of items inserted"
 8) (integer) 1
 9) "Number of items deleted"
10) (integer) 0
11) "Bucket size"
12) (integer) 4
13) "Expansion rate"
14) (integer) 2
15) "Max iterations"
16) (integer) 10

dragonfly> CF.INFO no_such_key
(error) ERR no such key
```

## See also

[`CF.RESERVE`](./cf.reserve.md) | [`CF.COUNT`](./cf.count.md)
