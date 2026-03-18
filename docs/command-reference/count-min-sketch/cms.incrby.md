---
description: Learn how to use the CMS.INCRBY command to increment the count of one or more items in a Count-Min Sketch.
---

import PageTitle from '@site/src/components/PageTitle';

# CMS.INCRBY

<PageTitle title="Redis CMS.INCRBY Command (Documentation) | Dragonfly" />

## Syntax

    CMS.INCRBY key item increment [item increment ...]

**Time complexity:** O(n) where n is the number of items

**ACL categories:** @cms

Increments the count of one or more `item`s in the Count-Min Sketch stored at `key` by the given `increment` values.
If `key` does not exist, a new sketch is created with default dimensions before incrementing.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array of integers, one per item, representing the estimated count of each item after the increment.

## Examples

```shell
dragonfly> CMS.INITBYDIM cms_key 2000 5
OK

dragonfly> CMS.INCRBY cms_key item1 1 item2 5
1) (integer) 1
2) (integer) 5

dragonfly> CMS.INCRBY cms_key item1 10
1) (integer) 11
```

## See also

[`CMS.INITBYDIM`](./cms.initbydim.md) | [`CMS.INITBYPROB`](./cms.initbyprob.md) | [`CMS.QUERY`](./cms.query.md) | [`CMS.MERGE`](./cms.merge.md)
