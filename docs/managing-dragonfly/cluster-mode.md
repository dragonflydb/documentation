---
sidebar_position: 5
---

# Cluster Mode

Dragonfly has 2 Cluster Modes:

1. Emulated cluster: a single Dragonfly node, usually helpful when migrating from Redis Cluster
2. Multi node cluster: joins multiple Dragonfly servers to a single data store

## Emulated Cluster

A single Dragonfly instance can achieve the same capacity as a multi node Redis Cluster.
In order to help with migrating an application from a Redis Cluster to Dragonfly, Dragonfly can
emulate a Redis Cluster.

```bash
# Running Dragonfly instance in cluster mode
$ dragonfly --cluster_mode=emulated
$ redis-cli 
# See which cluster commands are supported
127.0.0.1:6379> cluster help
```

Now you can connect to your Dragonfly instance with a Redis Cluster client, here's a Python example:
```python
>>> import redis
>>> r = redis.RedisCluster(host='localhost', port=6379)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

Note that your application code may be using a Redis client that does not require cluster commands,
in this case you don't need to specify the `--cluster_mode` flag.

In case you need to migrate data from Redis Cluster to Dragonfly you may find [Redis
Riot](https://developer.redis.com/explore/riot/) helpful.

## Multi Node Cluster

Sometimes vertical scaling is not enough. In those cases, you'll need to set up a Dragonfly Cluster.

A Dragonfly Cluster is similar to a Redis Cluster:

* Multiple Dragonfly servers participate in a single logical data store
* It provides all cluster-related commands required by Redis client libraries
* It [distributes keys](https://redis.io/docs/reference/cluster-spec/#key-distribution-model) in the
  same way Redis does
* It supports [hash tags](https://redis.io/docs/reference/cluster-spec/#hash-tags)

**Any client-side code that uses Redis Cluster should be able to migrate to Dragonfly Cluster with
no changes.** Dragonfly Cluster is similar to Redis Cluster in all client facing behavior but it
does not self managed as Redis Cluster in which nodes communicate with each other to discover
cluster setup and state

Setting up and managing a Dragonfly Cluster is different from managing a Redis Cluster.  Unlike
Redis, Dragonfly nodes do not communicate with each other (except for replication). Nodes are
unaware of other nodes being unavailable, and cluster configuration is done separately to each node.

Dragonfly only provides a _data plane_ (which is the Dragonfly server), but we do **not** provide a
_control plane_ to manage cluster deployments.

Follow the below steps to set up a Dragonfly Cluster

### Start Dragonfly Nodes

Start the Dragonfly nodes you need. Use the flags you would have used otherwise, but make sure to
add the following (to both masters and replicas):
* `--cluster_mode=yes` to let the nodes know that they are part of a cluster.
* `--admin_port=X`, where `X` is some port that you'll use to run _admin commands_. This port should
  generally not be exposed to users.

Note: when started in cluster mode, nodes will reply with errors to any user requests until they are
properly configured.

### Configure Replication

Replication is configured just like non-cluster replication, by using the `REPLICAOF` command. Note
that this is a necessary step even though this information is present in the cluster configuration
(see below).

### Configure Nodes

Note: Configuring cluster nodes is done by sending management commands via the _admin port_.
Dragonfly will refuse to handle cluster management commands via the regular port.

Cluster configuration includes information necessary for the cluster nodes to have in order to
operate, like which nodes participate in the cluster (and in what role), which node owns which
slots, etc.

The first thing you'll need to do is to get each node's _id_, which is a unique string identifying
the node. The id can be retrieved by issuing the command `DFLYCLUSTER MYID` on each of the nodes.

Once you have all of the IDs, build the configuration string (see below) and pass it to all nodes
using the `DFLYCLUSTER CONFIG <str>` command.

Once a server is configured, it will only handle the slots which it owns. This means that any keys
not owned by it will be deleted, and any attempts to access such keys will be rejected.

Dragonfly servers do not communicate with other servers to make sure all config is identical. It is
important to pass the exact same configuration to all nodes.

Configuration is a JSON-encoded string in the following format:

```json
[  // Array of node-entries
  {  // Node #1
    "slot_ranges": [
      { "start": X1, "end": Y1 },  // Slots [X1, Y1) owned by node 1
      { "start": X2, "end": Y2 }   // Slots [X2, Y2) are also owned by node 1
    ],
    "master": {
      "id": "...",  // Returned from DFLYCLUSTER MYID
      "ip": "...",  // The IP or hostname that *clients* should use to access this node
      "port": ...   // The port that *clients* should use to access this node
    },
    "replicas": [  // Replicas use the same fields as the master config
      { "id": "...", "ip": "...", port: ... },  // First replica for node
      { "id": "...", "ip": "...", port: ... }   // Second replica for node
    ]
  },
  { ... }, // Node #2
  { ... }, // Node #3, etc
]
```

Here is an example of a cluster config with 2 master nodes, each with 1 replica:

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
         "port": ...
      },
      "replicas": [
         {
            "id": "...",
            "ip": "...",
            "port": ...
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
         "port": ...
      },
      "replicas": [
         {
            "id": "...",
            "ip": "...",
            "port": ...
         }
      ]
   }
]
```

You'll need to resend the configuration to nodes after restart, and to update all nodes with new
configuration upon any changes to the cluster, such as adding / removing nodes, changing hostnames,
etc.

### Final Notes

* Cluster mode is still in development. Please file issues if suspect you've found a bug.
* You could look at
  [`cluster_mgr.py`](https://github.com/dragonflydb/dragonfly/blob/main/tools/cluster_mgr.py) as a
  reference for how to set up and configure a cluster. This script starts a cluster _locally_, but
  much of its logic can be reused for nodes present on remote machines as well.
* Dragonfly does not yet support migration of slots data between nodes. Changing slot allocation
  will result in data removal.
