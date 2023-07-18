---
sidebar_position: 4
---

# Replication

## Managing Replicas

Dragonfly supports a primary/secondary replication model, similarly to Redis’s [replication](https://redis.io/topics/replication). When using replication, Dragonfly creates exact copies of the primary instance. Once configured properly, secondary instances reconnect to the primary any time their connections break and will always aim to remain an exact copy of the primary.

Dragonfly replication management API is compatible with Redis API and consists of two user-facing commands: ROLE and REPLICAOF (SLAVEOF).

If you’re not sure whether the Dragonfly instance you’re currently connected to is a primary instance or a replica, you can check by running the  `role ` command:

```bash
role
```

This command will return either  `master ` or  `replica `.

## Redis/Dragonfly replication
Dragonfly supports Redis -> Dragonfly replication to allow a convenient migration of Redis workloads to Dragonfly. We currently support data structures and replication protocol of Redis OSS up to version 6.2. The instructions below apply to this type of replication as well with only difference that the primary instance is a running Redis server.

## Dragonfly/Dragonfly replication
This replication process internally is vastly different from the original Redis replication algorithm, but from the outside, the API is kept the same to make it compatible with the current ecosystem.

To designate a Dragonfly instance as a replica of another instance on the fly, run the  `replicaof ` command. This command takes the intended primary server’s hostname or IP address and port as arguments:

```bash
replicaof hostname_or_IP port
```

If the server is already a replica of another primary, it will stop replicating the old server and immediately start synchronizing with the new one. It will also discard the old dataset.

To promote a replica back to being a primary, run the following `replicaof` command:
```bash
replicaof no one
```

This will stop the instance from replicating the primary server but will not discard the dataset it has already replicated. This syntax is useful in cases where the original primary fails. After running `replicaof no one` on a replica of the failed primary, the former replica can be used as the new primary and have its own replicas as a failsafe.

## Monitoring Lag

Dragonfly defines the replication lag as the maximum amount of unacknowledged database changes over all the shards. This metric is calculated by the master instance and is visible both as the `dfly_connected_replica_lag_records` field in the [prometheus metrics](./monitoring.md), and through the `INFO REPLICATION` command.
