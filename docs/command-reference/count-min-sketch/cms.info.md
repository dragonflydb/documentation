---
description: Learn how to use the CMS.INFO command to retrieve information about a Count-Min Sketch.
---

import PageTitle from '@site/src/components/PageTitle';

# CMS.INFO

<PageTitle title="Redis CMS.INFO Command (Documentation) | Dragonfly" />

## Syntax

    CMS.INFO key

**Time complexity:** O(1)

**ACL categories:** @cms

Returns metadata about the Count-Min Sketch stored at `key`, including its dimensions and the total number of counted events.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): A flat array of field-value pairs with the following fields:

- `width`: The number of counters in each row.
- `depth`: The number of hash functions / rows.
- `count`: The total sum of all increments applied to the sketch.

## Examples

```shell
dragonfly> CMS.INITBYDIM cms_key 2000 5
OK

dragonfly> CMS.INCRBY cms_key item1 10 item2 3
1) (integer) 10
2) (integer) 3

dragonfly> CMS.INFO cms_key
1) width
2) (integer) 2000
3) depth
4) (integer) 5
5) count
6) (integer) 13
```

## See also

[`CMS.INITBYDIM`](./cms.initbydim.md) | [`CMS.INITBYPROB`](./cms.initbyprob.md) | [`CMS.QUERY`](./cms.query.md) | [`CMS.MERGE`](./cms.merge.md)
