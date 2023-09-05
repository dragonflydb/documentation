---
sidebar_position: 5
---

# Memcached Mode

Use the `memcached_port` flag to select a port for exposing the Memcached-compatible interface. By default, it is disabled.
For example, to run on Memcached's default port, use:

```shell
$> ./dragonfly --logtostderr --memcached_port 11211
```

By running the command above, Dragonfly allows you to use the Redis and Memcached APIs simultaneously:

```text
AcceptServer - listening on port 11211
AcceptServer - listening on port 6379
```

## Keyspace Sharing

It is notable that the Memcached API shares the same keyspace with the Redis logical database `0`.

```shell
# Set a key in Redis logical database '0', which is the default database.
dragonfly-redis$> SET my_key_db_ZERO 1000
OK

# Switch to Redis logical database '1'.
dragonfly-redis$> SELECT 1
OK

# Database '1' has no keys.
dragonfly-redis$> KEYS *
(empty array)

# Set a key in Redis logical database '1'.
dragonfly-redis$> SET my_key_db_ONE 1000
OK
```

```shell
# Try to read the key 'my_key_db_ZERO' via the Memcached API.
# This works since the key exists in Redis logical database '0'.
dragonfly-memcached$> get my_key_db_ZERO
VALUE my_key_db_ZERO 0 4
1000
END

# Try to read the key 'my_key_db_ONE' via the Memcached API.
# The key is not found since it only exists in Redis logical database '1'.
dragonfly-memcached$> get my_key_db_ONE 
END
```
