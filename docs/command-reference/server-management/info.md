---
description: Learn how to use Redis INFO command to yield information and statistics of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# INFO

<PageTitle title="Redis INFO Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `INFO` command in Redis is used to retrieve various pieces of information and statistics about the server. This includes memory usage, client connections, replication status, CPU usage, and more. It is typically used for monitoring and debugging purposes.

## Syntax

```cli
INFO [section]
```

## Parameter Explanations

- **section**: (Optional) Specifies the section of information to return. Possible values include:
  - `server`: General information about the Redis server.
  - `clients`: Client connections information.
  - `memory`: Memory usage details.
  - `persistence`: RDB and AOF status.
  - `stats`: General statistics.
  - `replication`: Master/slave status.
  - `cpu`: CPU consumption.
  - `commandstats`: Command statistics.
  - `cluster`: Cluster information.
  - `keyspace`: Database-related statistics.
  - `all`: All of the above sections.
  - `default`: Default set of sections.

## Return Values

The `INFO` command returns a bulk string formatted as a series of lines containing property names and their values. Each line is terminated by a newline character (`\n`). For example:

```txt
# Server
redis_version:6.2.5
redis_git_sha1:00000000
redis_git_dirty:0
os:Linux 4.15.0-142-generic x86_64

# Clients
connected_clients:10
client_longest_output_list:0
client_biggest_input_buf:0
blocked_clients:0

...
```

## Code Examples

Using the CLI:

```cli
dragonfly> INFO server
# Server
redis_version:6.2.5
redis_git_sha1:00000000
redis_git_dirty:0
os:Linux 4.15.0-142-generic x86_64
...

dragonfly> INFO memory
# Memory
used_memory:1024000
used_memory_human:1000K
used_memory_rss:2048000
...

dragonfly> INFO all
# Server
redis_version:6.2.5
...

# Clients
connected_clients:10
...

# Memory
used_memory:1024000
...

# Persistence
loading:0
...
```

## Best Practices

- Regularly check the `memory` section to monitor and manage your Redis instance's memory usage.
- Use the `stats` and `commandstats` sections to identify performance bottlenecks or unusual activity.
- Automate the collection of `INFO` outputs for continuous monitoring and alerting.

## Common Mistakes

- Not specifying a section when only specific information is needed can lead to an overload of data, making it harder to find relevant information.
- Ignoring crucial metrics such as memory usage and replication status, which can lead to undiagnosed issues.

## FAQs

### What information does the `INFO` command provide?

The `INFO` command provides detailed information on different aspects of the Redis server, including server configuration, memory usage, client connections, replication status, and more.

### How can I use the `INFO` command to debug performance issues?

You can use the `INFO stats` and `INFO commandstats` commands to get insights into server operations and command execution times, which can help in identifying and addressing performance bottlenecks.

### Can I limit the output of the `INFO` command?

Yes, you can limit the output by specifying a section. For example, `INFO memory` will only return memory-related statistics.
