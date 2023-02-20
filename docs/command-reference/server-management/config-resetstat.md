---
description: Reset the stats returned by INFO
---

# CONFIG RESETSTAT

## Syntax

    CONFIG RESETSTAT 

**Time complexity:** O(1)

Resets the statistics reported by Redis using the `INFO` command.

These are the counters that are reset:

* Keyspace hits
* Keyspace misses
* Number of commands processed
* Number of connections received
* Number of expired keys
* Number of rejected connections
* Latest fork(2) time
* The `aof_delayed_fsync` counter

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): always `OK`.
