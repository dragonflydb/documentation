---
description: Learn how to use Redis BF.EXISTS command to check for existence of an item in the bloom filter.
---
import PageTitle from '@site/src/components/PageTitle';

# BF.EXISTS

<PageTitle title="Redis BF.EXISTS Command (Documentation) | Dragonfly" />

## Syntax

    BF.EXISTS key item

**Time complexity:** O(1)


**ACL categories:** @bloom

Checks for an existense of a single item in a Bloom filter <code>key</code>

## Returns
[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): 1 if the element probably exists,
0 if it definitely does not exist.

## Examples

```shell
dragonfly> BF.EXISTS bf Hello
(integer) 1
```

## See also

`BF.ADD` | `BF.MEXISTS`

