---
description: "Learn how the Redis READWRITE command works in Dragonfly, where it replies OK only in emulated cluster mode."
---

import PageTitle from '@site/src/components/PageTitle';

# READWRITE

<PageTitle title="Redis READWRITE Command (Documentation) | Dragonfly" />

## Syntax

    READWRITE

**Time complexity:** O(1)

**ACL categories:** @connection, @fast

In Valkey, `READWRITE` turns off the read-only mode that [`READONLY`](./readonly.md) turns on
for a connection to a cluster replica.

Dragonfly has no per-connection read-only mode, so `READWRITE` does not change the connection.
With `--cluster_mode=emulated`, it replies `OK`.
With cluster mode off, it returns `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` with `--cluster_mode=emulated`.

[Error reply](https://valkey.io/topics/protocol/#simple-errors): with cluster mode off.

## Examples

A node started with `--cluster_mode=emulated`:

```shell
dragonfly> READWRITE
OK
```

## See also

[`READONLY`](./readonly.md) | [`CLUSTER`](./cluster.md) | [Cluster Mode](../../managing-dragonfly/cluster-mode.md)
