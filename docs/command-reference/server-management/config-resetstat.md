---
description:  Learn how to use Redis CONFIG RESETSTAT command to reset statistics of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG RESETSTAT

<PageTitle title="Redis CONFIG RESETSTAT Command (Documentation) | Dragonfly" />

## Syntax

    CONFIG RESETSTAT

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

Resets the statistics reported by Dragonfly using the `INFO` command.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): always `OK`.
