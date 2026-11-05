---
description: "Dragonfly's emulated single-shard and multi-shard cluster modes."
sidebar_position: 5
---

# Cluster Mode

Dragonfly has the following cluster modes:

- **Emulated Single-Shard Cluster**: a single Dragonfly node, usually helpful when migrating to Dragonfly from Redis Cluster.
- **Multi-Shard Cluster**: joins multiple Dragonfly servers to a single distributed in-memory data store.

## Emulated Single-Shard Cluster

A single Dragonfly instance can usually achieve the same capacity (memory size and QPS) as a multi-node Redis Cluster.
In order to help with migrating an application from a Redis Cluster to Dragonfly, Dragonfly can emulate a Redis Cluster.

```bash
# Running a Dragonfly instance in the emulated cluster mode.
$> dragonfly --cluster_mode=emulated

# Connecting to the Dragonfly instance using Redis-CLI.
$> redis-cli

# Check the cluster state
dragonfly> CLUSTER INFO
```

See [`CLUSTER`](../command-reference/cluster-management/cluster.md) for the supported cluster subcommands.

Now you can connect to your Dragonfly instance with a Redis client that supports the Redis Cluster protocol,
here's how it would look like in Python using [redis-py](https://github.com/redis/redis-py):

```python
>>> import redis
>>> r = redis.RedisCluster(host='localhost', port=6379)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

### Notes

- Your application code may be using a regular Redis client that does not require cluster commands as well.
- Cluster mode is disabled by default: if the `--cluster_mode` server flag is not specified,
  `CLUSTER` commands return `ERR Cluster is disabled. Enabled via passing --cluster_mode=emulated|yes`.
- In emulated mode, `cluster_announce_ip` and `announce_port` can be changed at runtime with `CONFIG SET`.
  Subsequent cluster topology replies use the new values.
- In emulated mode, replicas advertise the master's announced address in cluster topology replies.

## Multi-Shard Cluster

### Overview

Sometimes vertical scaling is not enough. In those cases, you'll need to set up a Dragonfly multi-shard cluster.
For simplicity, we will refer to the multi-shard topology as Dragonfly Cluster.

A Dragonfly Cluster is similar to a Redis/Valkey Cluster:

- Multiple Dragonfly servers participate in a single logical data store.
- It provides all cluster-related commands required by Redis client libraries.
- It [distributes keys](https://valkey.io/topics/cluster-spec/) in the same way as Valkey Cluster.
- It supports [hash tags](https://valkey.io/topics/cluster-spec/#hash-tags) in the same way as Valkey Cluster.

**There is one important distinction regarding Dragonfly Cluster:**
Dragonfly only provides a _data plane_ (which is the Dragonfly server), but it does **NOT** provide a
_control plane_ to manage cluster deployments. Tasks like node health monitoring, automatic failover,
slot migration for data rebalancing, and others are out of the scope of Dragonfly server functionality
and are provided as part of the [Dragonfly Cloud](https://www.dragonflydb.io/cloud) service,
namely, [Dragonfly Swarm](#dragonfly-swarm).

Any client-side code that uses Redis Cluster should be able to migrate to Dragonfly Cluster with
no changes. Dragonfly Cluster is similar to Redis Cluster in all client-facing behavior, but it
does not self-manage as Redis Cluster does, in which nodes communicate with each other to discover
cluster setup and state. You can read more about the architectural differences [here](https://www.dragonflydb.io/blog/redis-and-dragonfly-cluster-design-comparison).

Setting up and managing a Dragonfly Cluster is different from managing a Redis Cluster.
Unlike Redis, Dragonfly nodes do not communicate with each other, except for replication and slot migration.

Follow the below steps to set up a Dragonfly Cluster.

### Start Dragonfly Nodes

Start the Dragonfly nodes you need. Use the flags you would have used otherwise, but make sure to
add the following (to both masters and replicas):

- `--cluster_mode=yes` to let the nodes know that they are part of a cluster.
- `--admin_port=X`, where `X` is a port that you'll use to run _admin commands_.
  Note that this port generally should **NOT** be exposed to your data store users.
- `--cluster_node_id=ID`, where `ID` is a unique string that identifies the node in the cluster configuration.
  The node keeps this ID across restarts. Without this flag, the node generates a new random ID every time it starts.

When a Dragonfly server is started in cluster mode,
it will reply with errors to any user requests until the cluster is properly configured.

### Configure Replication

Replication is configured just like non-cluster replication, by using the `REPLICAOF` command. Note
that this is a necessary step even though this information is present in the cluster configuration
(see below).

### Configure Nodes

Configuring cluster nodes is done by sending management commands via the _admin port_.
It is advised to use a dedicated admin port for management-related commands.

Cluster configuration includes information necessary for the cluster nodes to have in order to
operate, like which nodes participate in the cluster (and in what role, primary or replica),
which node owns which hash slots, etc.

The following are the major commands and steps you need in order to configure a Dragonfly Cluster:

- `CLUSTER MYID`:
  The first thing you'll need to do is to get each node's ID, which is a unique string identifying
  the node. The ID can be retrieved by issuing the command
  [`CLUSTER MYID`](../command-reference/cluster-management/cluster-myid.md) on each of the nodes.
  For a node started with `--cluster_node_id`, the ID is the value of this flag.
- `DFLYCLUSTER CONFIG`:
  Once you have all of the IDs, build the configuration string (see below) and pass it to all nodes
  using the `DFLYCLUSTER CONFIG` command. Note that this command takes a **JSON-encoded string** as the parameter.

Once a Dragonfly server is configured, it will only handle the slots that it owns.
This means that any keys not owned by it will be deleted, and any attempts to access such keys will be rejected.

Dragonfly servers do not communicate with other servers to make sure all config is identical.
It is important to pass the exact same configuration to all nodes.

The configuration is a JSON-encoded string in the following format:

```json
[
   {
      "slot_ranges": [
         {
            "start": 0,
            "end": 16383
         }
      ],
      "master": {
         "id": "node-1",
         "ip": "10.0.0.1",
         "port": 6379,
         "health": "online"
      },
      "replicas": [
         {
            "id": "node-2",
            "ip": "10.0.0.2",
            "port": 6379,
            "health": "online"
         }
      ],
      "migrations": []
   }
]
```

It is an array with one entry per shard: a master/primary node, its replicas, and the hash slots they own.
Each entry has the following fields:

- `slot_ranges`: the hash slots owned by the shard. Ranges are inclusive: `{ "start": 0, "end": 8191 }`
  covers slots `0` through `8191`. Every slot from `0` to `16383` must be owned by exactly one shard.
- `master`: the master/primary node.
- `replicas`: the replicas of the master/primary node. Replicas use the same fields as the master.
  This field is required. Use an empty array (`[]`) for a shard without replicas.
- `migrations`: optional, the outgoing
  [slot migrations](../command-reference/cluster-management/dflycluster-config.md#slot-migration) of the shard.

The master and each replica have the following fields:

- `id`: the node ID, returned by `CLUSTER MYID`.
- `ip`: the IP or hostname that clients should use to access this node.
- `port`: the port that clients should use to access this node, as a number.
- `health`: optional, the state that cluster topology replies report for the node:
  `online` (the default), `loading`, `fail` or `hidden`. For example,
  [`CLUSTER SLOTS`](../command-reference/cluster-management/cluster-slots.md) lists only the replicas that are `online`.

The configuration must be valid JSON: keys are quoted, and comments and trailing commas are not allowed.

Here is an example of a Dragonfly Cluster configuration with 2 master/primary nodes, each with 1 replica,
for nodes started with `--cluster_node_id` set to `node-1` through `node-4`:

```json
[
   {
      "slot_ranges": [
         {
            "start": 0,
            "end": 8191
         }
      ],
      "master": {
         "id": "node-1",
         "ip": "10.0.0.1",
         "port": 6379
      },
      "replicas": [
         {
            "id": "node-2",
            "ip": "10.0.0.2",
            "port": 6379
         }
      ]
   },
   {
      "slot_ranges": [
         {
            "start": 8192,
            "end": 16383
         }
      ],
      "master": {
         "id": "node-3",
         "ip": "10.0.0.3",
         "port": 6379
      },
      "replicas": [
         {
            "id": "node-4",
            "ip": "10.0.0.4",
            "port": 6379
         }
      ]
   }
]
```

You'll need to resend the configuration to nodes after restart and to update all nodes
with the new configuration upon any changes to the cluster,
such as adding/removing nodes, changing hostnames, etc.
A node started with `--cluster_node_id` keeps its ID across restarts, so you can resend the same configuration.
Otherwise, the node gets a new random ID every time it starts: update the configuration with the new ID
and send it to all nodes. A master whose ID is not in the configuration owns no slots and deletes all of its keys.

### Notes

- Multi-shard cluster mode supports only database 0.
- You could look at
  [`cluster_mgr.py`](https://github.com/dragonflydb/dragonfly/blob/main/tools/cluster_mgr.py) as a
  reference for how to set up and configure a cluster. This script starts a cluster locally, but
  much of its logic can be reused for nodes present on remote machines as well.
- If you're getting errors trying to issue the `DFLYCLUSTER CONFIG`, check Dragonfly's logs (if you
  can pass `--logtostderr` temporarily) to see why the config was rejected.
- `DFLYMIGRATE` is rejected unless cluster mode is enabled.
- Dragonfly supports the migration of data slots between nodes as well. A detailed explanation can
  be found in one of our blog posts [here](https://www.dragonflydb.io/blog/redis-and-dragonfly-cluster-design-comparison).
  The configuration fields of a migration are described in
  [`DFLYCLUSTER CONFIG`](../command-reference/cluster-management/dflycluster-config.md#slot-migration).

## Dragonfly Swarm

Dragonfly server provides a powerful data plane and crucial admin commands to configure
and join a Dragonfly Cluster. However, it does not include a built-in
control plane for cluster management. This flexibility allows you to create your own control plane
or leverage community-driven solutions if demand arises.

To simplify cluster management in the cloud, we introduce **Dragonfly Swarm** as part of
our cloud offering, an all-in-one solution for seamless Dragonfly Cluster operations.
Dragonfly Swarm offers:

- **Automated Management**: Just choose your desired amount of memory to provision, which can also be
  adjusted later. From there, sharding, slot migration, data rebalancing,
  and everything else are automatically managed.
- **Cloud-Native Integration**: Optimized for major cloud providers including AWS, GCP, and Azure.
- **High Availability**: Built-in failover for zero downtime.
- **Monitoring and Analytics**: Real-time insights into cluster performance.
- **Simplified Operations**: Intuitive tools for configuration, maintenance, and scaling.

Dragonfly Swarm lets you focus on your applications while handling the complexities of cluster management.
Check out the [cloud documentation](../cloud/datastores.md#cluster-mode) to see how easy it is
to configure and manage your Dragonfly Swarm data stores.
