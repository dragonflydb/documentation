---
description: Learn how to use Redis BF.RESERVE to create a new bloom filter entry in Dragonfly.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.RESERVE

<PageTitle title="Redis BF.RESERVE Command (Documentation) | Dragonfly" />

## Syntax

    BF.RESERVE  key false_positive_rate capacity

**Time complexity:** O(1)


**ACL categories:** @bloom

Creates a new bloom filter with the initial capacity of at least `capacity`,
 and false positive rate `false_positive_rate` that should be a double
 between `0` and `0.5`.

## Returns
[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` if `SET` was executed correctly.

## Examples

```shell
dragonfly> BF.RESERVE bf 0.0001 500000
"OK"
```

## See also
`BF.ADD`

