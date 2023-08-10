---
sidebar_position: 1
description: Use the `REPLICAOF` command for migration
---

# Replication

## Overview

Replication is a versatile migration technique that offers a robust way to transition data between database instances.
This strategic approach revolves around the establishment of a dynamic primary-replica relationship.
Within this approach, data originating from the source Redis instance is meticulously replicated onto a designated replica instance,
in this case the new Dragonfly instance, ensuring the continuity of information within a newly configured environment.

One notable advantage is that Dragonfly can be directly employed as a replication target for a Redis instance.
Underneath the replication mechanism, an initial snapshot of the existing dataset is taken, capturing a specific point in time.
This snapshot serves as the foundation upon which the replication process builds.
However, it's important to note that the ongoing writes after the snapshot are also captured by the replication mechanism.
This distinctive advantage ensures that the replica stays current and reflects the most recent updates made on the source Redis instance.

## Migration Steps

In the following example, we will assume that:

- The source Redis instance runs with the hostname **`redis-source`** and the port number **`6379`**.
- The new Dragonfly instance runs with the hostname **`dragonfly`** and the port number **`6380`**.

### 1. Set Up Replication

Initiate the migration by establishing a primary-replica relationship between the source Redis instance and the new Dragonfly instance.
This ensures that changes made on the source Redis instance are automatically propagated to the replica.

On the Redis source instance, check its replication information:

```shell
redis-source-6379$> INFO replication
# Replication
role:master
connected_slaves:0
master_replid:b728e54c84b190ed555817e1d05c4d932a145f45
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:15302
master_repl_meaningful_offset:0
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:15302
```

On the new Dragonfly instance, use the [`REPLICAOF`](../../command-reference/server-management/replicaof.md) command to instruct itself to replicate data from the source:

```shell
dragonfly-6380$> REPLICAOF redis-source 6379
"OK"
```

After the primary-replica relationship is established, you should see data replicated into the new Dragonfly instance.
We can check the replication information again on both instances:

```shell
redis-source-6379$> INFO replication
# Replication
role:master
connected_slaves:1
slave0:ip=172.xx.x.4,port=6380,state=online,offset=15693,lag=2
master_replid:b728e54c84b190ed555817e1d05c4d932a145f45
master_replid2:0000000000000000000000000000000000000000
master_repl_offset:15693
master_repl_meaningful_offset:15441
second_repl_offset:-1
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:1
repl_backlog_histlen:15693
```

```shell
dragonfly-6380$> INFO replication
# Replication
role:replica
master_host:redis-source
master_port:6379
master_link_status:up
master_last_io_seconds_ago:8
master_sync_in_progress:0
```

### 2. Decommission the Source Redis Instance

Once replication is active and data synchronization between the primary (`redis-source`) and replica (`dragonfly`) is confirmed, the old primary instance can be decommissioned.
This is achieved by promoting the new Dragonfly instance to become the new primary.
Use the command [`REPLICAOF NO ONE`](../../command-reference/server-management/replicaof.md) on the Dragonfly instance to break the replication link from the source:

```shell
dragonfly-6380$> REPLICAOF NO ONE
"OK"

dragonfly-6380$> INFO replication
# Replication
role:master
connected_slaves:0
master_replid:d612ca7db5cfb8cdb19bac01155faf645e5ab8df
```

### 3. Reconfigure and Restart Applications

After successfully promoting the new Dragonfly instance to the role of primary, it's essential to reconfigure your server applications to connect to Dragonfly.
This step involves modifying your applications' configuration to point to the Dragonfly instance instead of the previous Redis instance.

## Considerations

By employing the Replication migration technique, you ensure data continuity while seamlessly transitioning to a new database instance. However, it's important to be aware of potential challenges and considerations:

- **Downtime:** In comparison with the [Snapshot and Restore](./00-snapshot-and-restore.md) technique, the Replication migration technique is able to capture ongoing writes from the source instance. **Reconfiguration and restarting your server applications are still needed, although the downtime window could be significantly smaller than Snapshot and Restore.**

- **Network Latency:** Replicating data across instances involves network communication, which might introduce latency. Ensure that network connectivity and performance are optimized to minimize any delays.

- **Data Consistency:** While replication strives to maintain data consistency between the primary and replica, it's crucial to verify that the replication process is complete and synchronized before decommissioning the old master.

- **Replica Lag:** In some cases, replica instances might lag behind the primary due to factors like network issues or resource limitations. Monitoring replica lag and addressing any discrepancies is essential to maintain data integrity.

- **Impact on Performance:** Replication can have an impact on the performance of the primary instance, especially if there's a high volume of write operations. Monitor the performance of both the primary and replica instances to ensure optimal functionality.

The Replication migration technique offers a powerful solution for transitioning data between database instances.
By following these steps and considering potential challenges, you can seamlessly migrate your data while minimizing disruptions to your applications and users.
