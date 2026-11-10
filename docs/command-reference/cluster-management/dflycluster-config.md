---
description: "Apply a JSON configuration that assigns hash slots to the masters and replicas of a Dragonfly multi-shard cluster."
---

import PageTitle from '@site/src/components/PageTitle';

# DFLYCLUSTER CONFIG

<PageTitle title="Dragonfly DFLYCLUSTER CONFIG Command (Documentation) | Dragonfly" />

## Syntax

    DFLYCLUSTER CONFIG config

**Time complexity:** O(N) where N is the size of the configuration. If a master stops owning some slots, a background task then scans all of its keys to delete the keys of those slots.

**ACL categories:** @admin, @dangerous, @slow

The `DFLYCLUSTER CONFIG` command applies a cluster configuration to the current node.
`config` is a JSON array with one object per shard: the shard's slot ranges, its master and its replicas.
See [Cluster Mode](../../managing-dragonfly/cluster-mode.md) for the format and for how to set up a cluster.

The command requires `--cluster_mode=yes`.
Otherwise, including with `--cluster_mode=emulated`, it returns `ERR Cluster is disabled. Use --cluster_mode=yes to enable.`

Dragonfly nodes do not exchange their configuration.
Send the same configuration to every node of the cluster, masters and replicas, whenever the cluster changes.

The configuration identifies each node by the ID that [`CLUSTER MYID`](./cluster-myid.md) returns.
Unless the node is started with [`--cluster_node_id`](../../managing-dragonfly/flags.md#--cluster_node_id),
this ID is random and changes on every restart.
A node does not keep its configuration across restarts, so send it a configuration again after it restarts.
If the node's ID changed, list the new ID: a configuration from before the restart no longer lists the node,
and a master that applies it deletes all of its keys, including the keys that it loaded from a snapshot at startup.

Until a node receives its first configuration, commands that access keys return `ERR Cluster is not yet configured`.
After the node applies a configuration:

- It serves the slots of the shard that lists its ID, as the master or as a replica.
  Commands on keys of other slots return a `MOVED` redirection to the master of the slot,
  at the `ip` and `port` from the configuration.
- A master deletes, in the background, the keys of the slots that it no longer owns,
  and its replicas delete them through replication.
  A master whose ID is missing from the configuration owns no slots and deletes all of its keys.
- [`CLUSTER SHARDS`](./cluster-shards.md), [`CLUSTER SLOTS`](./cluster-slots.md) and
  [`CLUSTER NODES`](./cluster-nodes.md) report the new topology.

Sending the configuration that the node already has changes nothing and returns `OK`.

## Admin port

Send `DFLYCLUSTER CONFIG` to the port that [`--admin_port`](../../managing-dragonfly/flags.md#--admin_port) opens,
and do not expose that port to clients. By default, the main port accepts the command too.
To accept it only on the admin port, start the node with
[`--restricted_commands=DFLYCLUSTER`](../../managing-dragonfly/flags.md#--restricted_commands),
or with `--restricted_commands=DFLYCLUSTER,DFLYMIGRATE` to restrict slot migration traffic as well.
The main port then returns `ERR Cannot execute restricted command (admin only)`.

## Validation

The node rejects the whole configuration with `ERR Invalid cluster configuration.` and keeps its current one if:

- `config` is not valid JSON. Comments and trailing commas are not allowed.
- A slot from `0` to `16383` belongs to no shard or to more than one shard.
  Slot ranges are inclusive: `"start": 0, "end": 8191` covers slots `0` through `8191`.
- A slot range has a `start` greater than its `end`, or a slot greater than `16383`.
- A shard has no `replicas` array. The array can be empty.
- A node does not have a string `id`, a string `ip` and a numeric `port`.
  A port written as a string, such as `"6379"`, is rejected.
- A node's `health` is not one of `online`, `loading`, `fail` and `hidden`. The values are case-insensitive.
- A node ID appears more than once.
- A `migrations` entry is invalid, for example its target is not the master of another shard
  or its slots do not belong to the shard.

The server log shows why a configuration was rejected.

## Slot migration

A shard's optional `migrations` list moves slots from the shard's master to the master of another shard.
Each entry has the `node_id` of the target master, the `ip` and `port` that the source connects to,
and the `slot_ranges` to move, which must belong to the shard.
The source talks to the target with `DFLYMIGRATE` commands, so if the target restricts `DFLYMIGRATE`,
`port` must be the target's admin port.
Follow the migration with [`DFLYCLUSTER SLOT-MIGRATION-STATUS`](./dflycluster-slot-migration-status.md).
When it reaches `FINISHED`, send a configuration that assigns the migrated slots to the target's shard
and no longer lists the migration. The source then deletes the migrated keys.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` when the configuration is applied.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): if the configuration is invalid,
the configuration argument is missing or followed by more arguments,
the node does not run with `--cluster_mode=yes`, or the command is restricted to the admin port.

## Examples

A single node started with `--cluster_mode=yes --admin_port=6380`, connected through its admin port.
This configuration makes the node the master of all slots:

```json
[
  {
    "slot_ranges": [ { "start": 0, "end": 16383 } ],
    "master": { "id": "d2f90c64b7a89bc60edb3a7ceb5d66eb10f32184", "ip": "192.168.215.30", "port": 6379 },
    "replicas": []
  }
]
```

`DFLYCLUSTER CONFIG` takes the configuration as one argument, so `redis-cli` needs it on one line, in single quotes.
The node ID is random and the IP address is the node's own, so the values vary:

```shell
dragonfly> CLUSTER MYID
d2f90c64b7a89bc60edb3a7ceb5d66eb10f32184
dragonfly> SET foo bar
(error) ERR Cluster is not yet configured
dragonfly> DFLYCLUSTER CONFIG '[{"slot_ranges":[{"start":0,"end":16383}],"master":{"id":"d2f90c64b7a89bc60edb3a7ceb5d66eb10f32184","ip":"192.168.215.30","port":6379},"replicas":[]}]'
OK
dragonfly> SET foo bar
OK
dragonfly> GET foo
"bar"
```

A configuration that leaves slots `8192` to `16383` unassigned is rejected:

```shell
dragonfly> DFLYCLUSTER CONFIG '[{"slot_ranges":[{"start":0,"end":8191}],"master":{"id":"d2f90c64b7a89bc60edb3a7ceb5d66eb10f32184","ip":"192.168.215.30","port":6379},"replicas":[]}]'
(error) ERR Invalid cluster configuration.
```

## See also

[`DFLYCLUSTER GETSLOTINFO`](./dflycluster-getslotinfo.md) | [`DFLYCLUSTER FLUSHSLOTS`](./dflycluster-flushslots.md) | [`DFLYCLUSTER SLOT-MIGRATION-STATUS`](./dflycluster-slot-migration-status.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
