---
description: "Learn how to use Redis CLUSTER MYID command to get the node ID that a Dragonfly node uses in cluster mode."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER MYID

<PageTitle title="Redis CLUSTER MYID Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER MYID

**Time complexity:** O(1)

**ACL categories:** @slow

The `CLUSTER MYID` command returns the ID of the current node.
The same ID identifies the node in the replies of [`CLUSTER NODES`](./cluster-nodes.md),
[`CLUSTER SHARDS`](./cluster-shards.md) and [`CLUSTER SLOTS`](./cluster-slots.md).
The command requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

- With `--cluster_mode=yes`, the ID is the value of [`--cluster_node_id`](../../managing-dragonfly/flags.md#--cluster_node_id).
  If the flag is empty (the default), the ID is the random 40-character hex replication ID
  that the node generates on every start. While the node is a master, `INFO replication`
  shows the same value as `master_replid`.
  Set `--cluster_node_id` to keep the ID stable across restarts.
  Use this ID as the node's `id` in the configuration that you send with [`DFLYCLUSTER CONFIG`](./dflycluster-config.md).
- With `--cluster_mode=emulated`, the ID is always this random replication ID.
  Setting `--cluster_node_id` in this mode is unsupported:
  Dragonfly logs `Setting --cluster_node_id in emulated mode is unsupported` and exits.

The ID does not change while the process runs, even when the node's replication role changes.

Valkey returns the ID as a bulk string; Dragonfly returns a simple string.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): the node ID.

## Examples

With `--cluster_mode=emulated`, the ID is random, so the output varies:

```shell
dragonfly> CLUSTER MYID
ff05becf27ee3e6e8caea2acbf8a943b42989e73
```

Dragonfly started with `--cluster_mode=yes --cluster_node_id=node-a`:

```shell
dragonfly> CLUSTER MYID
node-a
```

## See also

[`CLUSTER NODES`](./cluster-nodes.md) | [`DFLYCLUSTER CONFIG`](./dflycluster-config.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
