---
description: "Learn how to use Redis CLUSTER INFO command to get the cluster state, slot coverage and node counts of a Dragonfly node."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER INFO

<PageTitle title="Redis CLUSTER INFO Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER INFO

**Time complexity:** O(N + R) where N is the number of nodes and R is the number of slot ranges in the cluster topology

**ACL categories:** @slow

The `CLUSTER INFO` command returns the cluster state as seen by the current node, in the same
`field:value` format as Valkey. It requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

Dragonfly reports the following fields:

| Field | Value in Dragonfly |
|---|---|
| `cluster_state` | `ok` when the node has a topology: always with `--cluster_mode=emulated`, and with `--cluster_mode=yes` after the node receives its configuration with [`DFLYCLUSTER CONFIG`](./dflycluster-config.md). `fail` before that. |
| `cluster_slots_assigned`, `cluster_slots_ok` | `16384` when `cluster_state` is `ok`, otherwise `0`. A configuration must cover all slots, or `DFLYCLUSTER CONFIG` rejects it. |
| `cluster_slots_pfail`, `cluster_slots_fail` | Always `0`, even when the configuration sets the `health` of a node to `fail`. |
| `cluster_known_nodes` | The number of masters and replicas in the topology, or `0` before the node is configured. Replicas whose `health` in the configuration is `hidden` are counted, although `CLUSTER NODES`, `CLUSTER SHARDS` and `CLUSTER SLOTS` do not list them. |
| `cluster_size` | The number of shards that own at least one slot, or `0` before the node is configured. |
| `cluster_current_epoch`, `cluster_my_epoch` | Always `1`. |
| `cluster_stats_messages_*` | Fixed values. Dragonfly nodes do not exchange cluster bus messages. |

In emulated mode, the topology is the node and its replicas, or, on a replica, its master and the replica itself.
See [`CLUSTER`](./cluster.md) for both modes.

Valkey also reports `total_cluster_links_buffer_limit_exceeded`; Dragonfly does not.

## Return

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): `field:value` lines separated by CRLF.
Dragonfly sends a bulk string under RESP3 as well, where Valkey sends a
[verbatim string](https://valkey.io/topics/protocol/#verbatim-strings).

## Examples

A node started with `--cluster_mode=emulated` and no replicas:

```shell
dragonfly> CLUSTER INFO
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:1
cluster_size:1
cluster_current_epoch:1
cluster_my_epoch:1
cluster_stats_messages_ping_sent:1
cluster_stats_messages_pong_sent:1
cluster_stats_messages_sent:1
cluster_stats_messages_ping_received:1
cluster_stats_messages_pong_received:1
cluster_stats_messages_meet_received:0
cluster_stats_messages_received:1
```

## See also

[`CLUSTER NODES`](./cluster-nodes.md) | [`CLUSTER SHARDS`](./cluster-shards.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
