---
description: "Learn how to use Redis CLUSTER NODES command to get the cluster topology that a Dragonfly node reports, one line per node."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER NODES

<PageTitle title="Redis CLUSTER NODES Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER NODES

**Time complexity:** O(N + R) where N is the number of nodes and R is the number of slot ranges in the cluster topology

**ACL categories:** @slow

The `CLUSTER NODES` command returns the cluster topology as seen by the current node, as text with one line per node.
It requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

- With `--cluster_mode=emulated`, the topology is a single shard that owns all slots, `0-16383`.
  On a master, it lists the node itself, followed by the replicas connected to it
  (with `--managed_service_info`, the replicas are listed only to connections on the admin port).
  The master reports its own address as the address that the client connected to and its `--port`;
  [`--cluster_announce_ip`](../../managing-dragonfly/flags.md#--cluster_announce_ip) and
  [`--announce_port`](../../managing-dragonfly/flags.md#--announce_port) override them.
  On a replica, it lists the master that the replica replicates from, followed by the replica itself.
- With `--cluster_mode=yes`, the topology is the configuration that the node received with
  [`DFLYCLUSTER CONFIG`](./dflycluster-config.md), and the addresses are the ones in that configuration.
  Until the first configuration, the command returns `ERR Cluster is not yet configured`.

Each line has the following fields, separated by spaces:

```text
<id> <ip>:<port>@<port> <flags> <master> 0 0 0 <link-state> <slot-range> ...
```

- `id`: the node ID, as returned by [`CLUSTER MYID`](./cluster-myid.md) on that node.
- `ip:port@port`: the node's address. The port after `@`, which is the cluster bus port in Valkey, is the same as the client port.
- `flags`: `master` or `slave`. On the line of the current node, the flags start with `myself,`, for example `myself,master`.
- `master`: `-` on a master line. On a replica line, the ID of its master.
- `0 0 0`: the ping-sent, pong-received and config-epoch fields, which are always `0`.
- `link-state`: `connected`, or `disconnected` for a node whose `health` in the configuration is `fail`.
- `slot-range`: on a master line, the slot ranges of the shard, each as `start-end` (inclusive),
  or as a single number for a range of one slot. Replica lines have no slots.

Each line ends with a newline character (`\n`).
Replicas whose `health` in the configuration is `hidden` are not listed.

Compared to Valkey, the flags are only `myself`, `master` and `slave`,
and slots that are being migrated or imported are not marked.

## Return

[Bulk string reply](https://valkey.io/topics/protocol/#bulk-strings): the cluster topology, one line per node.
Dragonfly sends a bulk string under RESP3 as well, where Valkey sends a
[verbatim string](https://valkey.io/topics/protocol/#verbatim-strings).

## Examples

A node started with `--cluster_mode=emulated` and no replicas.
The node ID is random and the address depends on the connection, so the output varies:

```shell
dragonfly> CLUSTER NODES
73c9a2cf4cadb357ce2878b765c396a50f3f3ac8 192.168.215.11:6379@6379 myself,master - 0 0 0 connected 0-16383
```

The first master of a cluster of nodes started with `--cluster_mode=yes`.
The configuration has two shards: the first owns slots `0-8191` and has one replica, the second owns slots `8192-16383`.
The node IDs and addresses come from the configuration, so they vary:

```shell
dragonfly> CLUSTER NODES
50f7b857ca92af62ef5b2c48ecbe1af7758aaa6b 192.168.107.2:6379@6379 myself,master - 0 0 0 connected 0-8191
c31d1462436ca637ac7d4d2009e5f1db79c4c0f5 192.168.107.4:6379@6379 slave 50f7b857ca92af62ef5b2c48ecbe1af7758aaa6b 0 0 0 connected
fa1ae4f79abb4951dfb7b0be792866a9eea741c1 192.168.107.3:6379@6379 master - 0 0 0 connected 8192-16383
```

## See also

[`CLUSTER SHARDS`](./cluster-shards.md) | [`CLUSTER SLOTS`](./cluster-slots.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
