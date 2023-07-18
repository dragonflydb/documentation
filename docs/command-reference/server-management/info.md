---
description: Get information and statistics about the server
---

# INFO

## Syntax

    INFO [section [section ...]]

**Time complexity:** O(1)

The `INFO` command returns information and statistics about the server in a
format that is simple to parse by computers and easy to read by humans.

The optional parameter can be used to select a specific section of information:

*   `server`: General information about the Dragonfly server
*   `clients`: Client connections section
*   `memory`: Memory consumption related information
*   `persistence`: Persistence related information
*   `stats`: General statistics
*   `replication`: Master/replica replication information
*   `cpu`: CPU consumption statistics
*   `commandstats`: Command statistics
*   `keyspace`: Database related statistics
*   `errorstats`: Error statistics

It can also take the following values:

*   `all`: Return all sections (excluding module generated ones)

When no parameter is provided, the `default` option is assumed.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): as a collection of text lines.

Lines can contain a section name (starting with a # character) or a property.
All the properties are in the form of `field:value` terminated by `\r\n`.

``` bash
dragonfly> INFO
# Server
redis_version:df-dev
redis_mode:standalone
arch_bits:64
multiplexing_api:iouring
tcp_port:6379
uptime_in_seconds:9
uptime_in_days:0

# Clients
connected_clients:1
client_read_buf_capacity:256
blocked_clients:0

# Memory
used_memory:67219536
used_memory_human:64.11MiB
used_memory_peak:67219536
comitted_memory:134963200
used_memory_rss:128823296
used_memory_rss_human:122.86MiB
object_used_memory:27
table_used_memory:66189280
num_buckets:1720320
num_entries:1005001
inline_keys:1005001
strval_bytes:0
updateval_amount:0
listpack_blobs:0
listpack_bytes:0
small_string_bytes:0
pipeline_cache_bytes:0
maxmemory:3169176780
maxmemory_human:2.95GiB
cache_mode:store

# Stats
total_connections_received:1
total_commands_processed:2
instantaneous_ops_per_sec:0
total_pipelined_commands:0
total_net_input_bytes:14
total_net_output_bytes:11249
instantaneous_input_kbps:-1
instantaneous_output_kbps:-1
rejected_connections:-1
expired_keys:0
evicted_keys:0
hard_evictions:0
garbage_checked:0
garbage_collected:0
bump_ups:0
stash_unloaded:0
traverse_ttl_sec:0
delete_ttl_sec:0
keyspace_hits:0
keyspace_misses:0
total_reads_processed:1
total_writes_processed:1850
async_writes_count:0
parser_err_count:0
defrag_attempt_total:0
defrag_realloc_total:0
defrag_task_invocation_total:0

# Replication
role:master
connected_slaves:0
master_replid:5114684b4a5bc1ab7fa9133c5ac972028c62f576

# Keyspace
db0:keys=1005001,expires=0,avg_ttl=-1

# CPU
used_cpu_sys:0.76107
used_cpu_user:9.353156
used_cpu_sys_children:0.0
used_cpu_user_children:0.0
used_cpu_sys_main_thread:0.32040
used_cpu_user_main_thread:4.681903
```

## Notes

Please note depending on the version of Dragonfly some of the fields have been
added or removed. A robust client application should therefore parse the
result of this command by skipping unknown properties, and gracefully handle
missing fields.

Here is the meaning of all fields in the **server** section:

*   `redis_version`: Version of the Dragonfly server
*   `redis_mode`: The server's mode ("standalone", "sentinel" or "cluster")
*   `arch_bits`: Architecture (32 or 64 bits)
*   `multiplexing_api`: Event loop mechanism used by Dragonfly
*   `tcp_port`: TCP/IP listen port
*   `uptime_in_seconds`: Number of seconds since Dragonfly server start
*   `uptime_in_days`: Same value expressed in days

Here is the meaning of all fields in the **clients** section:

*   `connected_clients`: Number of client connections (excluding connections
    from replicas)
*   `client_read_buf_capacity`: Client read buffer size in bytes.
*   `blocked_clients`: Number of clients pending on a blocking call (`BLPOP`,
    `BRPOP`, `BRPOPLPUSH`, `BLMOVE`, `BZPOPMIN`, `BZPOPMAX`)

Here is the meaning of all fields in the **memory** section:

*   `used_memory`: Total number of bytes allocated by Dragonfly using its
    allocator
*   `used_memory_human`: Human readable representation of previous value
*   `used_memory_peak`: Peak memory consumed by Dragonfly (in bytes)
*   `used_memory_rss`: Number of bytes that Dragonfly allocated as seen by the
    operating system (a.k.a resident set size). This is the number reported by
    tools such as `top(1)` and `ps(1)`
*   `used_memory_rss_human`: Human readable representation of previous value
*   `maxmemory`: The value of the `maxmemory` configuration directive
*   `maxmemory_human`: Human readable representation of previous value

Ideally, the `used_memory_rss` value should be only slightly higher than
`used_memory`. When rss >> used, a large difference may mean there is (external) memory fragmentation.

When Dragonfly frees memory, the memory is given back to the allocator, and the
allocator may or may not give the memory back to the system. There may be
a discrepancy between the `used_memory` value and memory consumption as
reported by the operating system. It may be due to the fact memory has been
used and released by Dragonfly, but not given back to the system. The
`used_memory_peak` value is generally useful to check this point.

Here is the meaning of all fields in the **persistence** section:

* `last_save`: Epoch based timestamp of last successful save
* `last_save_duration_sec`: Duration of the last save operation in seconds
* `last_save_file`: File path of last save file

Here is the meaning of all fields in the **stats** section:

*   `total_connections_received`: Total number of connections accepted by the
    server
*   `total_commands_processed`: Total number of commands processed by the server
*   `instantaneous_ops_per_sec`: Number of commands processed per second
*   `total_pipelined_commands`: Total number of commands pipelined to the server
*   `total_net_input_bytes`: The total number of bytes read from the network
*   `total_net_output_bytes`: The total number of bytes written to the network
*   `instantaneous_input_kbps`: The network's read rate per second in KB/sec
*   `instantaneous_output_kbps`: The network's write rate per second in KB/sec
*   `rejected_connections`: Number of connections rejected because of `maxclients` limit
*   `expired_keys`: Total number of key expiration events
*   `evicted_keys`: Number of evicted keys due to `maxmemory` limit
*   `keyspace_hits`: Number of successful lookup of keys in the main dictionary
*   `keyspace_misses`: Number of failed lookup of keys in the main dictionary
*   `total_reads_processed`: Total number of read events processed
*   `total_writes_processed`: Total number of write events processed

Here is the meaning of all fields in the **replication** section:

*   `role`: Value is "master" if the instance is replica of no one, or "slave" if the instance is a replica of some master instance
*   `master_replid`: The replication ID of the Dragonfly server
*   `connected_slaves`: Number of connected replicas

If the instance is a replica, these additional fields are provided:

*   `master_host`: Host or IP address of the master
*   `master_port`: Master listening TCP port
*   `master_link_status`: Status of the link (up/down)
*   `master_last_io_seconds_ago`: Number of seconds since the last interaction
    with master
*   `master_sync_in_progress`: Indicate the master is syncing to the replica

For each replica, the following line is added:

*   `slaveXXX`: id, IP address, port

Here is the meaning of all fields in the **cpu** section:

*   `used_cpu_sys`: System CPU consumed by the Dragonfly server, which is the sum of system CPU consumed by all threads of the server process (main thread and background threads)
*   `used_cpu_user`: User CPU consumed by the Dragonfly server, which is the sum of user CPU consumed by all threads of the server process (main thread and background threads)
*   `used_cpu_sys_children`: System CPU consumed by the background processes
*   `used_cpu_user_children`: User CPU consumed by the background processes
*   `used_cpu_sys_main_thread`: System CPU consumed by the Dragonfly server main thread
*   `used_cpu_user_main_thread`: User CPU consumed by the Dragonfly server main thread

The **commandstats** section provides statistics based on the command type,
including the number of calls that reached command execution (not rejected),
the total CPU time consumed by these commands, the average CPU consumed
per command execution, the number of rejected calls
(errors prior command execution), and the number of failed calls
(errors within the command execution).

For each command type, the following line is added:

*   `cmdstat_XXX`: `XXX` - number of calls

The **keyspace** section provides statistics on the main dictionary of each
database.
The statistics are the number of keys, and the number of keys with an expiration.

For each database, the following line is added:

*   `dbXXX`: `keys=XXX,expires=XXX, avg_ttl=XXX`

[hcgcpgp]: http://code.google.com/p/google-perftools/
