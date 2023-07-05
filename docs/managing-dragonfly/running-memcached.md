---
sidebar_position: 5
---

# Running in Memcached mode

Use the `memcache_port` flag to select a port for exposing the Memcached compatible interface. By default it's disabled.

For example, to run on Memcached's default port, use

```
./dragonfly  --memcache_port 11211
```