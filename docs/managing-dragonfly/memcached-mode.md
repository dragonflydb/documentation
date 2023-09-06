---
sidebar_position: 5
---

# Memcached Mode

Use the `memcached_port` flag to select a port for exposing the Memcached-compatible interface. By default, it is disabled.
For example, to run on Memcached's default port, use:

```shell
$> ./dragonfly --logtostderr --memcached_port 11211
```

By running the command above, Dragonfly allows you to use both the Redis and Memcached APIs simultaneously:

```text
AcceptServer - listening on port 11211
AcceptServer - listening on port 6379
```

## Keyspace Sharing

It is notable that **the Memcached API shares the same keyspace with the Redis API logical database `0`**.
This is a designed behavior, which allows your backend services using different APIs to operate on the same set of data.
By doing so, a soft migration strategy can be achieved—you can gradually migrate individual services away from the Memcached API if that is ever desired.

However, Memcached doesn't support complex data types (lists, sets, sorted sets, hashes, etc.),
and it's not recommended to mix up operations from both APIs other than on the string data type.

```shell
# === Redis API === #
# Set a key in database '0', which is the default database.
dragonfly$> SET my_key_db_ZERO 1000
OK

# Switch to database '1'.
dragonfly$> SELECT 1
OK

# Database '1' has no keys.
dragonfly$> KEYS *
(empty array)

# Set a key in database '1'.
dragonfly$> SET my_key_db_ONE 1000
OK
```

```shell
# === Memcached API === #
# Try to read the key 'my_key_db_ZERO' via the Memcached API.
# This works since the key exists in database '0'.
dragonfly-memcached$> get my_key_db_ZERO
VALUE my_key_db_ZERO 0 4
1000
END

# Try to read the key 'my_key_db_ONE' via the Memcached API.
# The key is not found since it only exists in database '1'.
dragonfly-memcached$> get my_key_db_ONE 
END
```
