---
sidebar_position: 5
---

# Cluster Mode

Dragonfly can reach the capacity of a multi node Redis Cluster on a single instance.
In order to help with migrating an application from a Redis Cluster to Dragonfly, Dragonfly can emulate a Redis Cluster.

```bash
# Running Dragonfly instance in cluster mode
$ dragonfly --cluster_mode=emulated
$ redis-cli 
# See which cluster commands are supported
127.0.0.1:6379> cluster help
```

Note that your application code may be using a redis client that does not require cluster commands, in this case you don't need to specify the `--cluster_mode` flag.

[Redis Riot](https://developer.redis.com/explore/riot/) is a great tool for migrating date from a Redis Cluster to Dragonfly.