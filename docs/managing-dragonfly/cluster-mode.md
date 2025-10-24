---
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

# See which cluster commands are supported
dragonfly$> CLUSTER HELP
```

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
- By default, if the `--cluster_mode` server flag is not specified, Dragonfly runs in this emulated cluster mode.

## Multi-Shard Cluster

### Overview

Sometimes vertical scaling is not enough. In those cases, you'll need to set up a Dragonfly multi-shard cluster.
For simplicity, we will refer to the multi-shard topology as Dragonfly Cluster.

A Dragonfly Cluster is similar to a Redis/Valkey Cluster:

- Multiple Dragonfly servers participate in a single logical data store.
- It provides all cluster-related commands required by Redis client libraries.
- It [distributes keys](https://redis.io/docs/reference/cluster-spec/#key-distribution-model) in the same way Redis Cluster does.
- It supports [hash tags](https://redis.io/docs/latest/operate/oss_and_stack/reference/cluster-spec/#hash-tags) in the same way Redis Cluster does.

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

- `DFLYCLUSTER MYID`:
  The first thing you'll need to do is to get each node's ID, which is a unique string identifying
  the node. The ID can be retrieved by issuing the command `DFLYCLUSTER MYID` on each of the nodes.
- `DFLYCLUSTER CONFIG`:
  Once you have all of the IDs, build the configuration string (see below) and pass it to all nodes
  using the `DFLYCLUSTER CONFIG` command. Note that this command takes a **JSON-encoded string** as the parameter.

Once a Dragonfly server is configured, it will only handle the slots that it owns.
This means that any keys not owned by it will be deleted, and any attempts to access such keys will be rejected.

Dragonfly servers do not communicate with other servers to make sure all config is identical.
It is important to pass the exact same configuration to all nodes.

The configuration is a JSON-encoded string in the following format:

```json
[  // Array of node-entries.
  {  // Node #1
    "slot_ranges": [
      { "start": X1, "end": Y1 },  // Slots [X1, Y1) are owned by node 1.
      { "start": X2, "end": Y2 }   // Slots [X2, Y2) are also owned by node 1.
    ],
    "master": {
      "id": "...",   // Returned from DFLYCLUSTER MYID.
      "ip": "...",   // The IP or hostname that clients should use to access this node.
      "port": "..."  // The port that clients should use to access this node.
    },
    "replicas": [  // Replicas use the same fields as the master config.
      { "id": "...", "ip": "...", port: "..." },  // The first replica of the master/primary node.
      { "id": "...", "ip": "...", port: "..." }   // The second replica of the master/primary node.
    ]
  },
  { ... }, // Node #2
  { ... }, // Node #3, etc
]
```

Here is an example of a Dragonfly Cluster configuration with 2 master/primary nodes, each with 1 replica:

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
         "id": "...",
         "ip": "...",
         "port": "..."
      },
      "replicas": [
         {
            "id": "...",
            "ip": "...",
            "port": "..."
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
         "id": "...",
         "ip": "...",
         "port": "..."
      },
      "replicas": [
         {
            "id": "...",
            "ip": "...",
            "port": "..."
         }
      ]
   }
]
```

You'll need to resend the configuration to nodes after restart and to update all nodes
with the new configuration upon any changes to the cluster,
such as adding/removing nodes, changing hostnames, etc.

### Notes

- You could look at
  [`cluster_mgr.py`](https://github.com/dragonflydb/dragonfly/blob/main/tools/cluster_mgr.py) as a
  reference for how to set up and configure a cluster. This script starts a cluster locally, but
  much of its logic can be reused for nodes present on remote machines as well.
- If you're getting errors trying to issue the `DFLYCLUSTER CONFIG`, check Dragonfly's logs (you
  can pass `--logtostdout` temporarily) to see why the config was rejected.
- Dragonfly supports the migration of data slots between nodes as well. Detailed explaination can
  be found in one of our blog posts [here](https://www.dragonflydb.io/blog/a-preview-of-dragonfly-cluster).
  We will update the documentation to reflect these steps soon.

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
