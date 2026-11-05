---
description: "Learn how to use Redis CLUSTER SHARDS command to list the shards of a Dragonfly cluster with their slot ranges and nodes."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER SHARDS

<PageTitle title="Redis CLUSTER SHARDS Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER SHARDS

**Time complexity:** O(N + R) where N is the number of nodes and R is the number of slot ranges in the cluster topology

**ACL categories:** @slow

The `CLUSTER SHARDS` command returns the shards of the cluster as seen by the current node.
A shard is a set of hash slots served by one master and its replicas.
The command requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

- With `--cluster_mode=emulated`, the reply has a single shard that owns slots `0` to `16383`.
  On a master, its nodes are the node itself, followed by the replicas connected to it
  (with `--managed_service_info`, the replicas are listed only to connections on the admin port).
  The master reports its own address as the address that the client connected to and its `--port`;
  [`--cluster_announce_ip`](../../managing-dragonfly/flags.md#--cluster_announce_ip) and
  [`--announce_port`](../../managing-dragonfly/flags.md#--announce_port) override them.
  On a replica, its nodes are the master that the replica replicates from, followed by the replica itself.
- With `--cluster_mode=yes`, the reply lists the shards of the configuration that the node received with
  [`DFLYCLUSTER CONFIG`](./dflycluster-config.md), with the addresses from that configuration.
  Until the first configuration, the command returns `ERR Cluster is not yet configured`.

Each shard has two fields:

- `slots`: the slot ranges of the shard, as a flat list of start and end slots.
  Ranges are inclusive: `0` and `8191` stand for slots `0` through `8191`.
- `nodes`: the master, followed by its replicas.

Each node has the following fields:

- `id`: the node ID, as returned by [`CLUSTER MYID`](./cluster-myid.md) on that node.
- `endpoint` and `ip`: the node's address. Both fields have the same value.
- `port`: the port that clients connect to.
- `role`: `master` or `replica`.
- `replication-offset`: always `0`.
- `health`: `online`, `loading`, `fail` or `hidden`.
  With `--cluster_mode=emulated`, it is always `online`.
  With `--cluster_mode=yes`, it is the node's `health` in the configuration, `online` by default.
  Replicas whose `health` is `hidden` are not listed, so only a master can report `hidden`.

Shards and nodes are flat arrays of alternating field names and values, under RESP3 as well, where Valkey returns maps.
Compared to Valkey, shards have no `id` field, and nodes do not have the optional `hostname`, `tls-port` and `availability-zone` fields.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a nested list of shards, each with its slot ranges and nodes.

## Examples

A node started with `--cluster_mode=emulated` and no replicas.
The node ID is random and the address depends on the connection, so the output varies:

```shell
dragonfly> CLUSTER SHARDS
1) 1) "slots"
   2) 1) (integer) 0
      2) (integer) 16383
   3) "nodes"
   4) 1)  1) "id"
          2) "73c9a2cf4cadb357ce2878b765c396a50f3f3ac8"
          3) "endpoint"
          4) "192.168.215.11"
          5) "ip"
          6) "192.168.215.11"
          7) "port"
          8) (integer) 6379
          9) "role"
         10) "master"
         11) "replication-offset"
         12) (integer) 0
         13) "health"
         14) "online"
```

A node of a cluster of nodes started with `--cluster_mode=yes`.
The configuration has two shards: the first owns slots `0-8191` and has one replica, the second owns slots `8192-16383`.
The node IDs and addresses come from the configuration, so they vary:

```shell
dragonfly> CLUSTER SHARDS
1) 1) "slots"
   2) 1) (integer) 0
      2) (integer) 8191
   3) "nodes"
   4) 1)  1) "id"
          2) "50f7b857ca92af62ef5b2c48ecbe1af7758aaa6b"
          3) "endpoint"
          4) "192.168.107.2"
          5) "ip"
          6) "192.168.107.2"
          7) "port"
          8) (integer) 6379
          9) "role"
         10) "master"
         11) "replication-offset"
         12) (integer) 0
         13) "health"
         14) "online"
      2)  1) "id"
          2) "c31d1462436ca637ac7d4d2009e5f1db79c4c0f5"
          3) "endpoint"
          4) "192.168.107.4"
          5) "ip"
          6) "192.168.107.4"
          7) "port"
          8) (integer) 6379
          9) "role"
         10) "replica"
         11) "replication-offset"
         12) (integer) 0
         13) "health"
         14) "online"
2) 1) "slots"
   2) 1) (integer) 8192
      2) (integer) 16383
   3) "nodes"
   4) 1)  1) "id"
          2) "fa1ae4f79abb4951dfb7b0be792866a9eea741c1"
          3) "endpoint"
          4) "192.168.107.3"
          5) "ip"
          6) "192.168.107.3"
          7) "port"
          8) (integer) 6379
          9) "role"
         10) "master"
         11) "replication-offset"
         12) (integer) 0
         13) "health"
         14) "online"
```

## See also

[`CLUSTER SLOTS`](./cluster-slots.md) | [`CLUSTER NODES`](./cluster-nodes.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
