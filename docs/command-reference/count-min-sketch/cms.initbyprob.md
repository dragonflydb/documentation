---
description: Learn how to use the CMS.INITBYPROB command to initialize a Count-Min Sketch with a given error rate and probability.
---

import PageTitle from '@site/src/components/PageTitle';

# CMS.INITBYPROB

<PageTitle title="Redis CMS.INITBYPROB Command (Documentation) | Dragonfly" />

## Syntax

    CMS.INITBYPROB key error probability

**Time complexity:** O(1)

**ACL categories:** @cms

Initializes a Count-Min Sketch filter at `key` with dimensions automatically calculated from
the desired `error` rate and `probability` of accuracy.

- `error`: The desired error rate as a fraction of the total count. Must be a positive number between `0` and `1`.
  For example, `0.01` means the estimated count will be within `1%` of the true count.
- `probability`: The desired probability that an estimate will fall within the error bounds. Must be a positive number between `0` and `1`.
  For example, `0.999` means the estimate will be within the error bounds `99.9%` of the time.

If `key` already exists, an error is returned.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` if the sketch was created successfully.

## Examples

```shell
dragonfly> CMS.INITBYPROB cms_key 0.01 0.999
OK
```

## See also

[`CMS.INITBYDIM`](./cms.initbydim.md) | [`CMS.INCRBY`](./cms.incrby.md) | [`CMS.QUERY`](./cms.query.md) | [`CMS.INFO`](./cms.info.md)
