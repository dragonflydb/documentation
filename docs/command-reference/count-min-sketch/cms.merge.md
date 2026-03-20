---
description: Learn how to use the CMS.MERGE command to merge multiple Count-Min Sketches into a destination sketch.
---

import PageTitle from '@site/src/components/PageTitle';

# CMS.MERGE

<PageTitle title="Redis CMS.MERGE Command (Documentation) | Dragonfly" />

## Syntax

    CMS.MERGE destination numkeys source [source ...] [WEIGHTS weight [weight ...]]

**Time complexity:** O(n·w·d) where n is the number of source sketches, w is the width, and d is the depth

**ACL categories:** @cms

Merges multiple source Count-Min Sketches into `destination`.
The `destination` key must be pre-initialized via [`CMS.INITBYDIM`](./cms.initbydim.md) or [`CMS.INITBYPROB`](./cms.initbyprob.md) before calling this command — if it does not exist, an error is returned.
All sketches (sources and destination) must have identical `width` and `depth` dimensions. The destination's existing counts are overwritten.

- `numkeys`: The number of source sketch keys to merge.
- `source`: One or more source sketch keys.
- `WEIGHTS`: Optional integer multipliers applied to each source sketch before merging. Each source's counters are multiplied by its corresponding weight prior to being summed into the destination. Defaults to `1` for all sources if omitted.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the merge was successful.

## Examples

```shell
dragonfly> CMS.INITBYDIM cms1 2000 5
OK

dragonfly> CMS.INITBYDIM cms2 2000 5
OK

dragonfly> CMS.INCRBY cms1 item1 10 item2 3
1) (integer) 10
2) (integer) 3

dragonfly> CMS.INCRBY cms2 item1 5 item3 7
1) (integer) 5
2) (integer) 7

dragonfly> CMS.INITBYDIM cms_merged 2000 5
OK

dragonfly> CMS.MERGE cms_merged 2 cms1 cms2
OK

dragonfly> CMS.QUERY cms_merged item1 item2 item3
1) (integer) 15
2) (integer) 3
3) (integer) 7
```

Using `WEIGHTS` to scale contributions before merging:

```shell
dragonfly> CMS.INITBYDIM cms_weighted 2000 5
OK

dragonfly> CMS.MERGE cms_weighted 2 cms1 cms2 WEIGHTS 2 1
OK

dragonfly> CMS.QUERY cms_weighted item1 item2 item3
1) (integer) 25
2) (integer) 6
3) (integer) 7
```

## See also

[`CMS.INITBYDIM`](./cms.initbydim.md) | [`CMS.INITBYPROB`](./cms.initbyprob.md) | [`CMS.INCRBY`](./cms.incrby.md) | [`CMS.INFO`](./cms.info.md)
