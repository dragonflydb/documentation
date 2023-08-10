---
sidebar_position: 2
description: Use Sentinel for migration without downtime
---

# Sentinel

## Overview

In the preceding section, we delved into the [Replication](./01-replication.md) technique, which is a powerful approach employing the `REPLICAOF` command for reliable data transfer.
However, while this technique offers notable benefits, a minor drawback persists: the need for a downtime window, albeit a potentially brief one.
This necessitates reconfiguration and restarts of your server applications.

In this section, we ascend to the next level of sophistication by introducing an advanced technique: harnessing the capabilities of Redis Sentinel.
This technique promises to transcend the constraints of downtime, enabling you to execute a migration with uninterrupted service continuity.

## Redis Sentinel

Redis Sentinel stands as a distributed system designed to monitor and manage Redis instances, mainly geared towards achieving high availability and automatic failovers.
By orchestrating the deployment of multiple Redis instances, Sentinel ensures that your application can thrive amidst node failures, maintaining system robustness.
In essence, a Sentinel instance is just a Redis instance running in a special mode.
The ability to automatically handle failovers can be used to perform migrations as well.

## Migration Steps

At a high level, here are the steps involved:

- Start a new Dragonfly instance and configure it as a replica of the source (primary) Redis instance.
- Replicate data from the source (primary) Redis instance to the new Dragonfly instance.
- Allow replication to reach a steady state and monitor using the `INFO replication` command.
- Stop the primary Redis node and let Sentinel promote the Dragonfly instance to become the new primary.

As you can see, these steps are similar to the [Replication](./01-replication.md) technique.
The key difference here is to utilize Sentinel for the automatic and reliable transition, promoting the Dragonfly instance as the new primary.

In the following example, we will assume that:

- The source Redis instance runs with the hostname **`redis-source`** and the port number **`6379`**.
- The new Dragonfly instance runs with the hostname **`dragonfly`** and the port number **`6380`**.
- The Sentinel instance runs with the hostname **`sentinel`** and the port number **`5000`**.

### 1. Set Up Replication & Sentinel

Assume the original source Redis is running, and we can check its replication information:

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