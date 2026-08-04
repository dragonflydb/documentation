---
description: Learn how to use the CF.RESERVE command to create a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.RESERVE

<PageTitle title="CF.RESERVE Command (Documentation) | Dragonfly" />

## Syntax

    CF.RESERVE key capacity [BUCKETSIZE bucketsize] [MAXITERATIONS maxiterations] [EXPANSION expansion]

**Time complexity:** O(1)

**ACL categories:** @cuckoo_filter, @fast, @write

Creates a new Cuckoo filter at `key` using `capacity` as the initial sizing estimate.
If `key` already exists, an error is returned.

Unlike Bloom filters, Cuckoo filters support deletion of individual items.

## Parameters

| Parameter       | Default | Description                                                                                                        |
|-----------------|---------|--------------------------------------------------------------------------------------------------------------------|
| `key`           |         | The name of the filter.                                                                                            |
| `capacity`      |         | Initial sizing estimate. Dragonfly divides it by `BUCKETSIZE` and rounds the resulting base bucket count up to the next power of two, so the effective slot capacity can differ from this value. |
| `BUCKETSIZE`    | `2`     | Number of fingerprint slots per bucket. Higher values improve fill rate but increase false positive probability.   |
| `MAXITERATIONS` | `20`    | Maximum number of cuckoo-displacement attempts before declaring the filter full. Must be between 1 and 65535.     |
| `EXPANSION`     | `1`     | Growth factor for new sub-filters. `0` disables expansion; a nonzero value is rounded up to the next power of two. |

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the filter was created successfully.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` already exists, or a parameter is out of range.

## Examples

```shell
dragonfly> CF.RESERVE cf 1000
OK

dragonfly> CF.RESERVE cf 1000
(error) ERR item exists

dragonfly> CF.RESERVE cf_custom 10000 BUCKETSIZE 4 MAXITERATIONS 50 EXPANSION 2
OK
```

## See also

[`CF.ADD`](./cf.add.md) | [`CF.ADDNX`](./cf.addnx.md) | [`CF.INSERT`](./cf.insert.md) | [`CF.INFO`](./cf.info.md)
