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

- The source Redis instance runs with the hostname **`redis-source`**, the IP address **`200.0.0.1`**, and the port **`6379`**.
- The new Dragonfly instance runs with the hostname **`dragonfly`**, the IP address **`200.0.0.2`**, and the port **`6380`**.
- The Sentinel instance runs with the hostname **`sentinel`**, the IP address **`200.0.0.3`**, and the port **`5000`**.

### 1. Source Instance

Assume the original source Redis instance is running, and you can check its replication information:

```shell
redis-source:6379$> INFO replication
# Replication
role:master
connected_slaves:0
```

**Assume the source Redis instance is already managed by a Sentinel instance or a Sentinel cluster.
Otherwise, reconfiguration of your server applications is still needed which implies a potential downtime window.**
However, if your applications are running on a container orchestrator such as Kubernetes, the rolling update mechanism can help minimize the downtime.

### 2. Sentinel

**If your source Redis instance is not managed by Sentinel yet, follow the steps below.** Otherwise, continue to [Configure Replication](#3-configure-replication).

To start a Redis instance in Sentinel mode, you can use a minimal `sentinel.conf` file like the following:

```text
# sentinel.conf
port 5000
sentinel monitor master-instance 200.0.0.1 6379 1
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

Run a Redis instance in the Sentinel mode:

```shell
$> redis-server sentinel.conf --sentinel
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
    SentinelAddrs: []string{"200.0.0.3:5000"},
})
```

As shown in the snippet above, clients connect to the Sentinel-managed Redis not directly but via Sentinel instance(s).
The reason is that during a failover process, Sentinel needs to notify the clients about various of events and information such as:

- The primary instance is offline.
- Sentinel has promoted a new primary instance, and here is the network information.

The Sentinel-to-clients notification mechanism is powered by Pub/Sub, you can read more about Sentinel internals [here](https://redis.io/docs/management/sentinel/).
**Using a Sentinel-compatible client is essential to achieve the goal of zero-downtime migration.**

### 3. Configure Replication

With comprehensive introduction to Sentinel, the goal is still to migrate the Redis instance to a Dragonfly instance.
Start a new Dragonfly instance and use the [`REPLICAOF`](../../command-reference/server-management/replicaof.md) command to instruct itself to replicate data from the source:

```shell
dragonfly:6380$> REPLICAOF 200.0.0.1 6379
"OK"
```

After the primary-replica relationship is established, you should see data replicated into the new Dragonfly instance.
We can check the replication information again on both instances:

```shell
redis-source:6379$> INFO replication
# Replication
role:master
connected_slaves:1
slave0:ip=200.0.0.2,port=6380,state=online,offset=15693,lag=2
# ... more
# ... output
# ... omitted
```

```shell
dragonfly:6380$> INFO replication
# Replication
role:replica
master_host:200.0.0.1
master_port:6379
master_link_status:up
master_last_io_seconds_ago:8
master_sync_in_progress:0
```

Sentinel should also be aware of the primary Redis instance, as well as the new Dragonfly instance joining as a replica:

```shell
sentinel:5000$> SENTINEL get-master-addr-by-name master-instance
1) "200.0.0.1"
2) "6379"
```

```shell
sentinel:5000$> SENTINEL replicas master-instance
1)  1) "name"
    2) "200.0.0.2:6380"
    3) "ip"
    4) "200.0.0.2"
    5) "port"
    6) "6380"
# ... more
# ... output
# ... omitted
```

### 4. Failover to Replica