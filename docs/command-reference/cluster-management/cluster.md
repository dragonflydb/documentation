---
description: "Learn how to use Redis CLUSTER command to inspect the cluster topology and hash slots of a Dragonfly node."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER

<PageTitle title="Redis CLUSTER Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER

**Time complexity:** Depends on subcommand.

**ACL categories:** @slow

This is a container command for cluster introspection commands.
Cluster-aware clients use them to find out which nodes serve which hash slots.

Cluster mode is off by default. `CLUSTER` works only when Dragonfly is started with
[`--cluster_mode`](../../managing-dragonfly/flags.md#--cluster_mode) set to `emulated` or `yes`.
Otherwise, every subcommand returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.
[`INFO cluster`](../server-management/info.md) reports `cluster_enabled:1` when cluster mode is on and `cluster_enabled:0` when it is off.

- `--cluster_mode=emulated`: the node presents itself as a single-shard cluster that owns all 16384 hash slots.
  On a master, the topology replies also list the replicas connected to it
  (with `--managed_service_info`, only to connections on the admin port).
  On a replica, they list its master and the replica itself.
- `--cluster_mode=yes`: the topology comes from the configuration that the node receives with
  [`DFLYCLUSTER CONFIG`](./dflycluster-config.md).
  Until then, `CLUSTER NODES`, `CLUSTER SHARDS`, `CLUSTER SLOTS` and commands that access keys
  return `ERR Cluster is not yet configured`, and `CLUSTER INFO` reports `cluster_state:fail`.

See [Cluster Mode](../../managing-dragonfly/cluster-mode.md) for how to set up either mode.

Currently, the following subcommands are supported:

- [CLUSTER HELP](./cluster-help.md)
- [CLUSTER INFO](./cluster-info.md)
- [CLUSTER KEYSLOT](./cluster-keyslot.md)
- [CLUSTER MYID](./cluster-myid.md)
- [CLUSTER NODES](./cluster-nodes.md)
- [CLUSTER SHARDS](./cluster-shards.md)
- [CLUSTER SLOTS](./cluster-slots.md)

`CLUSTER HELP` describes only `SLOTS`, `NODES`, `INFO` and `HELP`, although all of the subcommands above work.

Dragonfly nodes do not exchange cluster state over a cluster bus, and slots are assigned with `DFLYCLUSTER CONFIG`.
The other Valkey subcommands, such as `CLUSTER ADDSLOTS`, `CLUSTER MEET`, `CLUSTER FAILOVER`, `CLUSTER RESET`,
`CLUSTER COUNTKEYSINSLOT`, `CLUSTER GETKEYSINSLOT`, `CLUSTER LINKS` and `CLUSTER MYSHARDID`, are not implemented.
They return an unknown-subcommand error, or a wrong-number-of-arguments error when called with arguments.

## Examples

Dragonfly started without `--cluster_mode`:

```shell
dragonfly> CLUSTER MYID
(error) ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes
```

Subcommands that Dragonfly does not implement, with `--cluster_mode=emulated`:

```shell
dragonfly> CLUSTER MYSHARDID
(error) ERR Unknown subcommand or wrong number of arguments for 'MYSHARDID'. Try CLUSTER HELP.
dragonfly> CLUSTER COUNTKEYSINSLOT 7000
(error) ERR wrong number of arguments for 'cluster countkeysinslot' command
```
