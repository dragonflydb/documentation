---
sidebar_position: 5
---

# Cluster Mode

A single Dragonfly instance can achieve the same capacity as a multi node Redis Cluster.
In order to help with migrating an application from a Redis Cluster to Dragonfly, Dragonfly can emulate a Redis Cluster.

```bash
# Running Dragonfly instance in cluster mode
$ dragonfly --cluster_mode=emulated
$ redis-cli 
# See which cluster commands are supported
127.0.0.1:6379> cluster help
```

Now you can connect to your Dragonfly instance with a Redis Cluster client, here's a python example:
```python
>>> import redis
>>> r = redis.RedisCluster(host='localhost', port=6379)
>>> r.set('foo', 'bar')
True
>>> r.get('foo')
b'bar'
```

Note that your application code may be using a redis client that does not require cluster commands, in this case you don't need to specify the `--cluster_mode` flag.

In case you need to migrate data from Redis Cluster to Dragonfly you may find [Redis Riot](https://developer.redis.com/explore/riot/) helpful.