---
description: Learn how to use Redis MEMORY STATS command to inspect Dragonfly memory statistics.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY STATS

<PageTitle title="Redis MEMORY STATS Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY STATS

**Time complexity:** O(number of connections)

**ACL categories:** @read, @slow

`MEMORY STATS` returns memory statistics collected by Dragonfly. The current
reply includes direct memory used by client connections and separate statistics
for replication connections:

- `connections.direct_bytes`
- `replication.connections_count`
- `replication.direct_bytes`

## Return

[Map reply](https://valkey.io/topics/protocol/#maps): memory-statistic names and
integer values in bytes, except for connection counts.

## Examples

```shell
dragonfly> MEMORY STATS
```
