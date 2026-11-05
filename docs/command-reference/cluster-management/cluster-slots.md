---
description: "Learn how to use Redis CLUSTER SLOTS command to map hash slot ranges to the Dragonfly nodes that serve them."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER SLOTS

<PageTitle title="Redis CLUSTER SLOTS Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER SLOTS

**Time complexity:** O(R × M) where R is the number of slot ranges in the cluster topology and M is the number of nodes in a shard

**ACL categories:** @slow

The `CLUSTER SLOTS` command returns the mapping of hash slot ranges to the nodes that serve them.
Cluster clients use it to find the node for each key.
The command requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

- With `--cluster_mode=emulated`, the reply has a single entry for slots `0` to `16383`.
  On a master, the entry lists the node itself, followed by the replicas connected to it
  (with `--managed_service_info`, the replicas are listed only to connections on the admin port).
  The master reports its own address as the address that the client connected to and its `--port`;
  [`--cluster_announce_ip`](../../managing-dragonfly/flags.md#--cluster_announce_ip) and
  [`--announce_port`](../../managing-dragonfly/flags.md#--announce_port) override them.
  On a replica, the entry lists the master that the replica replicates from, followed by the replica itself.
- With `--cluster_mode=yes`, the reply comes from the configuration that the node received with
  [`DFLYCLUSTER CONFIG`](./dflycluster-config.md), with the addresses from that configuration.
  Until the first configuration, the command returns `ERR Cluster is not yet configured`.

Each entry of the reply describes one slot range:

1. The first slot of the range.
2. The last slot of the range. Ranges are inclusive.
3. The master that serves the range.
4. The replicas of that master, one element each, if any.

Each node is an array of three elements: its IP address, its port and its node ID.
Valkey adds a fourth element with additional networking metadata, such as the hostname,
or an empty array when there is none; Dragonfly does not.

A shard with several slot ranges has one entry per range, and every entry lists the same nodes.
Replicas whose `health` in the configuration is `fail`, `loading` or `hidden` are not listed.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a nested list of slot ranges, each with the nodes that serve it.

## Examples

A node started with `--cluster_mode=emulated` and no replicas.
The node ID is random and the address depends on the connection, so the output varies:

```shell
dragonfly> CLUSTER SLOTS
1) 1) (integer) 0
   2) (integer) 16383
   3) 1) "192.168.215.11"
      2) (integer) 6379
      3) "73c9a2cf4cadb357ce2878b765c396a50f3f3ac8"
```

A node of a cluster of nodes started with `--cluster_mode=yes`.
The configuration has two shards: the first owns slots `0-8191` and has one replica, the second owns slots `8192-16383`.
The node IDs and addresses come from the configuration, so they vary:

```shell
dragonfly> CLUSTER SLOTS
1) 1) (integer) 0
   2) (integer) 8191
   3) 1) "192.168.107.2"
      2) (integer) 6379
      3) "50f7b857ca92af62ef5b2c48ecbe1af7758aaa6b"
   4) 1) "192.168.107.4"
      2) (integer) 6379
      3) "c31d1462436ca637ac7d4d2009e5f1db79c4c0f5"
2) 1) (integer) 8192
   2) (integer) 16383
   3) 1) "192.168.107.3"
      2) (integer) 6379
      3) "fa1ae4f79abb4951dfb7b0be792866a9eea741c1"
```

## See also

[`CLUSTER SHARDS`](./cluster-shards.md) | [`CLUSTER NODES`](./cluster-nodes.md) | [`CLUSTER KEYSLOT`](./cluster-keyslot.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
