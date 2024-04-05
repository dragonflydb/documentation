---
description: Learn how to use Redis BF.MEXISTS command to check for existence of item(s) in the bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.MEXISTS

<PageTitle title="Redis BF.MEXISTS Command (Documentation) | Dragonfly" />

## Syntax

    BF.MEXISTS key item [item ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @bloom

Checks for an existense of one or more items in a Bloom filter <code>key</code>

## Returns
[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): each element being the reply
as with `BF.EXISTS``.

## Examples

```shell
dragonfly> BF.MEXISTS bf Hello World
1) (integer) 1
2) (integer) 1
```

## See also

`BF.MADD` | `BF.EXISTS`

