---
description: "Learn how the Redis READONLY command works in Dragonfly, where it always replies OK and replicas serve reads without it."
---

import PageTitle from '@site/src/components/PageTitle';

# READONLY

<PageTitle title="Redis READONLY Command (Documentation) | Dragonfly" />

## Syntax

    READONLY

**Time complexity:** O(1)

**ACL categories:** @connection, @fast

In Valkey, `READONLY` lets a connection to a cluster replica read the keys of the replica's shard
instead of being redirected to the master.

Dragonfly accepts `READONLY` so that cluster clients can send it, but the command does nothing:
it always replies `OK` and does not change the connection.
This is the case in every mode, including when cluster mode is off.

Dragonfly replicas serve reads without `READONLY`:

- With `--cluster_mode=yes`, a replica that the cluster configuration lists in a shard serves
  reads of that shard's slots on every connection. Keys of other slots get a `MOVED` redirection.
- With `--cluster_mode=emulated`, or with cluster mode off, a replica serves reads of all keys.

Writes to a replica fail with `READONLY You can't write against a read only replica.`,
whether or not the connection sent `READONLY`.

[`READWRITE`](./readwrite.md) does not change the connection either.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`.

## Examples

```shell
dragonfly> READONLY
OK
```

A replica of a cluster of nodes started with `--cluster_mode=yes`.
The key `user:1000` (slot `1649`) belongs to the replica's shard, and its master set it to `alice`.
The replica serves the read without `READONLY` and rejects the write after it:

```shell
dragonfly> GET user:1000
"alice"
dragonfly> READONLY
OK
dragonfly> SET user:1000 bob
(error) READONLY You can't write against a read only replica.
```

## See also

[`READWRITE`](./readwrite.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md) | [Replication](../../managing-dragonfly/replication.md)
