---
description: Learn how to use the CF.RESERVE command to create a Cuckoo filter in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# CF.RESERVE

<PageTitle title="Redis CF.RESERVE Command (Documentation) | Dragonfly" />

## Syntax

    CF.RESERVE key capacity [BUCKETSIZE bucketsize] [MAXITERATIONS maxiterations] [EXPANSION expansion]

**Time complexity:** O(1)

**ACL categories:** @cuckoo

Creates a new Cuckoo filter at `key` with an initial capacity of at least `capacity` items.
If `key` already exists, an error is returned.

Unlike Bloom filters, Cuckoo filters support deletion of individual items.

## Parameters

| Parameter       | Default | Description                                                                                                        |
|-----------------|---------|--------------------------------------------------------------------------------------------------------------------|
| `key`           |         | The name of the filter.                                                                                            |
| `capacity`      |         | Estimated number of items the filter should hold. Actual capacity is rounded up to the next power of two.         |
| `BUCKETSIZE`    | `2`     | Number of fingerprint slots per bucket. Higher values improve fill rate but increase false positive probability.   |
| `MAXITERATIONS` | `20`    | Maximum number of cuckoo-displacement attempts before declaring the filter full. Must be between 1 and 65535.     |
| `EXPANSION`     | `1`     | When the filter is full, a new sub-filter of size `capacity * expansion` is created. `0` disables expansion.      |

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the filter was created successfully.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if `key` already exists, or a parameter is out of range.

## Examples

```shell
dragonfly> CF.RESERVE cf 1000
OK

dragonfly> CF.RESERVE cf 1000
(error) item exists

dragonfly> CF.RESERVE cf_custom 10000 BUCKETSIZE 4 MAXITERATIONS 50 EXPANSION 2
OK
```

