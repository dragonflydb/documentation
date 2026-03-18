---
description: Learn how to use the CMS.INITBYDIM command to initialize a Count-Min Sketch with given width and depth dimensions.
---

import PageTitle from '@site/src/components/PageTitle';

# CMS.INITBYDIM

<PageTitle title="Redis CMS.INITBYDIM Command (Documentation) | Dragonfly" />

## Syntax

    CMS.INITBYDIM key width depth

**Time complexity:** O(1)

**ACL categories:** @cms

Initializes a Count-Min Sketch filter at `key` with the given `width` and `depth` dimensions.

- `width`: The number of counters in each row (affects accuracy — a larger width reduces the error rate).
- `depth`: The number of hash functions / rows (affects confidence — a larger depth reduces the probability of error).

If `key` already exists, an error is returned.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the sketch was created successfully.

## Examples

```shell
dragonfly> CMS.INITBYDIM cms_key 2000 5
OK
```

## See also

[`CMS.INITBYPROB`](./cms.initbyprob.md) | [`CMS.INCRBY`](./cms.incrby.md) | [`CMS.QUERY`](./cms.query.md) | [`CMS.INFO`](./cms.info.md)
