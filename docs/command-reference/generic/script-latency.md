---
description: "Get the Redis SCRIPT LATENCY command to manage script evaluation latency."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT LATENCY

<PageTitle title="Redis SCRIPT LATENCY Command (Documentation) | Dragonfly" />

## Syntax

    SCRIPT LATENCY

**Time complexity:** O(N) with N being the number of called scripts.

**ACL categories:** @slow, @scripting

Prints latency histograms in usec for all called scripts.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays) This command returns an array of elements. The first element is the SHA1 digest of the scripts added into the script cache. The second element is latency historgram.
