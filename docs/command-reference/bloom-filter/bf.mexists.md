---
description: Learn how to use Redis BF.MEXISTS command to check for the existence of item(s) in the Bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.MEXISTS

<PageTitle title="Redis BF.MEXISTS Command (Documentation) | Dragonfly" />

## Syntax

    BF.MEXISTS key item [item ...]

**Time complexity:** O(1) for each item checked, so O(N) to check N items when the command is called with multiple arguments.

**ACL categories:** @bloom

Checks for the existence of one or more items in a Bloom filter `key`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays):
an array of integers, each representing the result for an individual item as if being processed by the [`BF.EXISTS`](./bf.exists.md) command:

- `1` if the item exists with a high probability.
- `0` if the item definitely does not exist.

## Examples

```shell
dragonfly> BF.MADD bf Hello World
1) (integer) 1
2) (integer) 1

dragonfly> BF.MEXISTS bf Hello World SomethingElse
1) (integer) 1
2) (integer) 1
3) (integer) 0
```

## See also

[`BF.MADD`](./bf.madd.md) | [`BF.EXISTS`](./bf.exists.md)
