---
description: Learn how to use Redis BF.ADD command to add an item to the bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.ADD

<PageTitle title="Redis BF.ADD Command (Documentation) | Dragonfly" />

## Syntax

    BF.ADD key item

**Time complexity:** O(1)


**ACL categories:** @bloom

Adds a single item to a Bloom filter <code>key</code>. The filter is created with default parameters
automatically if it did not exist before.

## Returns
[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): 1 if the element was added,
0 if it was added before.

## Examples

```shell
dragonfly> BF.ADD bf "Hello"
(integer) 1
```

## See also

`BF.RESERVE` | `BF.MADD`

