---
description: "Learn how to use Redis CLUSTER HELP command to list the CLUSTER subcommands and their descriptions in Dragonfly."
---

import PageTitle from '@site/src/components/PageTitle';

# CLUSTER HELP

<PageTitle title="Redis CLUSTER HELP Command (Documentation) | Dragonfly" />

## Syntax

    CLUSTER HELP

**Time complexity:** O(1)

**ACL categories:** @slow

The `CLUSTER HELP` command returns a helpful text describing the `CLUSTER` subcommands.

The text describes only `SLOTS`, `NODES`, `INFO` and `HELP`.
Dragonfly also supports [`CLUSTER KEYSLOT`](./cluster-keyslot.md), [`CLUSTER MYID`](./cluster-myid.md)
and [`CLUSTER SHARDS`](./cluster-shards.md), which the text leaves out.
See [`CLUSTER`](./cluster.md) for the full list.

Like every `CLUSTER` subcommand, `CLUSTER HELP` requires `--cluster_mode=emulated` or `--cluster_mode=yes`.
Otherwise, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a list of subcommands and their descriptions.

## Examples

```shell
dragonfly> CLUSTER HELP
 1) CLUSTER <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
 2) SLOTS
 3)    Return information about slots range mappings. Each range is made of:
 4)    start, end, master and replicas IP addresses, ports and ids.
 5) NODES
 6)    Return cluster configuration seen by node. Output format:
 7)    <id> <ip:port> <flags> <master> <pings> <pongs> <epoch> <link> <slot> ...
 8) INFO
 9)   Return information about the cluster
10) HELP
11)     Prints this help.
```

## See also

[`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
