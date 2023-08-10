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

- The source Redis instance runs with the hostname **`redis-source`**, the IP address **`77.1.63.79`**, and the port **`6379`**.
- The new Dragonfly instance runs with the hostname **`dragonfly`**, the IP address **`77.1.63.80`**, and the port **`6380`**.
- The Sentinel instance runs with the hostname **`sentinel`**, the IP address **`77.1.50.50`**, and the port **`5050`**.

### 1. Source Instance & Sentinel

Assume the original source Redis instance is running, and you can check its replication information:

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

**Assume the source Redis instance is already managed by a Sentinel instance or a Sentinel cluster.
Otherwise, reconfiguration of your server applications is still needed which implies a potential downtime window.**
However, if your applications are running on a container orchestrator such as Kubernetes, the rolling update mechanism can help minimize the downtime.

To start a Redis instance in Sentinel mode, you can use a minimal `sentinel.conf` file like the following:

```text
port 5000
sentinel monitor master-instance 77.1.63.79 6379 1
sentinel down-after-milliseconds master-instance 5000
sentinel failover-timeout master-instance 60000
```

The generalized form for the `sentinel monitor` configuration flag is as follows.
The example above is very minimal for illustration purpose only.
In a production environment, it is crucial to pick reasonable values for `quorum` and other configurable values.
Read more about Sentinel configuration [here](https://github.com/redis/redis/blob/unstable/sentinel.conf).

```text
sentinel monitor <master-name> <ip> <redis-port> <quorum>
```

Once the Sentinel instance and the Sentinel-managed Redis instance are running, it is important to confirm that the applications connect to them with the proper client.
Take the [go-redis](https://github.com/redis/go-redis) library as an example:

```go
import "github.com/redis/go-redis/v9"

// The <master-name> configuration has the value 'master-instance' in the 'sentinel.conf' file.
//
// There is only one Sentinel instance in our setup.
// In a production environment, multiple Sentinel instances with a reasonable 'quorum' value can be very important to achieve high availability.
client := redis.NewFailoverClient(&redis.FailoverOptions{
    MasterName:    "master-instance",
    SentinelAddrs: []string{"77.1.50.50:5050"},
})
```

As shown in the code snippet above, clients connect to the Sentinel-managed Redis not directly but via Sentinel instance(s).
The reason is that during a failover process, Sentinel needs to notify the clients about different events and information such as:

- The primary instance is offline.
- Sentinel has promoted a new primary instance, and here is the network information.

**Using a Sentinel-compatible client is essential to achieve the goal of zero-downtime migration.**

### 2. Set Up Replication