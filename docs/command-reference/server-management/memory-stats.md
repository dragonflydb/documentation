---
description:  Learn how to use the Redis MEMORY STATS command to inspect connection memory usage in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY STATS

<PageTitle title="Redis MEMORY STATS Command (Documentation) | Dragonfly" />

## Syntax

    MEMORY STATS

**Time complexity:** O(N) where N is the number of open connections.

**ACL categories:** @read, @slow

The `MEMORY STATS` command reports how much memory the server has allocated for connections,
separating regular client connections from replication flows.

The reply covers connection memory only. It does not mirror the much larger field set that Redis
returns, so figures such as peak allocation or dataset size are not part of it. For a breakdown of
overall server memory, use the `Memory` section of [`INFO`](./info.md); for allocator internals,
use [`MEMORY MALLOC-STATS`](./memory-malloc-stats.md) or [`MEMORY ARENA`](./memory-arena.md).

## Return

[Map reply](https://valkey.io/topics/protocol/#maps): the memory usage metrics listed below. Under
RESP2 the map is returned as a flat array of alternating field names and values.

| Field | Description |
| --- | --- |
| `connections.direct_bytes` | Bytes allocated for client connections, excluding replication connections. |
| `replication.connections_count` | Number of connections currently serving a replication flow. |
| `replication.direct_bytes` | Bytes allocated for those replication connections. |

## Examples

```shell
dragonfly> MEMORY STATS
1) "connections.direct_bytes"
2) (integer) 10936
3) "replication.connections_count"
4) (integer) 0
5) "replication.direct_bytes"
6) (integer) 0
```

Under RESP3 the same reply is rendered as a map:

```shell
dragonfly> MEMORY STATS
1# "connections.direct_bytes" => (integer) 10936
2# "replication.connections_count" => (integer) 0
3# "replication.direct_bytes" => (integer) 0
```

## See also

[`MEMORY`](./memory.md) | [`MEMORY USAGE`](./memory-usage.md) | [`MEMORY MALLOC-STATS`](./memory-malloc-stats.md) | [`INFO`](./info.md)
