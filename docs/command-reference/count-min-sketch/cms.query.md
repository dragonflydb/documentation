---
description: Learn how to use the CMS.QUERY command to retrieve the estimated count of one or more items from a Count-Min Sketch.
---

import PageTitle from '@site/src/components/PageTitle';

# CMS.QUERY

<PageTitle title="Redis CMS.QUERY Command (Documentation) | Dragonfly" />

## Syntax

    CMS.QUERY key item [item ...]

**Time complexity:** O(n) where n is the number of items

**ACL categories:** @cms

Returns the estimated count of one or more `item`s from the Count-Min Sketch stored at `key`.

The returned counts are estimates and may be higher than the true count (over-counting) due to hash collisions,
but will never be lower than the true count.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): An array of integers, one per item, representing the estimated count of each queried item.

## Examples

```shell
dragonfly> CMS.INITBYDIM cms_key 2000 5
OK

dragonfly> CMS.INCRBY cms_key item1 10 item2 3
1) (integer) 10
2) (integer) 3

dragonfly> CMS.QUERY cms_key item1 item2 item3
1) (integer) 10
2) (integer) 3
3) (integer) 0
```

## See also

[`CMS.INCRBY`](./cms.incrby.md) | [`CMS.INITBYDIM`](./cms.initbydim.md) | [`CMS.INITBYPROB`](./cms.initbyprob.md) | [`CMS.INFO`](./cms.info.md)
