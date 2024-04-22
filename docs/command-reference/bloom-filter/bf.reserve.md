---
description: Learn how to use Redis BF.RESERVE to create a new Bloom filter entry in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.RESERVE

<PageTitle title="Redis BF.RESERVE Command (Documentation) | Dragonfly" />

## Syntax

    BF.RESERVE key false_positive_rate capacity

**Time complexity:** O(1)

**ACL categories:** @bloom

Creates a new Bloom filter with an initial capacity of at least `capacity`
and a false positive rate `false_positive_rate` that should be a double between `0` and `0.5`.

## Returns

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` if the Bloom filter was created successfully.

## Examples

```shell
dragonfly> BF.RESERVE bf 0.0001 500000
OK
```

## See also

[`BF.ADD`](./bf.add.md) | [`BF.MADD`](./bf.madd.md)
