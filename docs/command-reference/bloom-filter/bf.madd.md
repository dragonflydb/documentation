---
description: Learn how to use Redis BF.MADD command to add an item to the bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.MADD

<PageTitle title="Redis BF.MADD Command (Documentation) | Dragonfly" />

## Syntax

    BF.MADD key item [item ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.


**ACL categories:** @bloom

Adds one or more item to a Bloom filter <code>key</code>

## Returns
[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): each element being the reply
as with `BF.ADD``.

## Examples

```shell
dragonfly> BF.MADD bf Hello World
1) (integer) 1
2) (integer) 1
```

## See also

`BF.RESERVE` | `BF.ADD`

