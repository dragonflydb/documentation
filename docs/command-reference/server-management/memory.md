---
description: Learn how to use Redis MEMORY command to fetch information on memory.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY

<PageTitle title="Redis MEMORY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MEMORY` command in Redis is used to inspect various memory-related metrics for a running Redis instance. It helps with understanding memory consumption, identifying memory leaks, and optimizing memory usage. Typical use cases include performance monitoring, debugging applications, and capacity planning.

## Syntax

The general syntax of the `MEMORY` command is as follows:

```plaintext
MEMORY [subcommand] [arguments]
```

## Parameter Explanations

- **subcommand**: The specific operation you want to perform. Common subcommands include:

  - **USAGE**: Reports the memory usage of a key.
  - **STATS**: Provides general statistics about the memory allocation of the Redis server.
  - **PURGE**: Clears the internal memory cache (called lazyfree).
  - **MALLOC-STATS**: Shows detailed low-level memory allocator statistics.
  - **HELP**: Lists all available subcommands and their descriptions.

- **arguments**: Additional parameters required by some subcommands (e.g., key names).

## Return Values

The return values vary depending on the subcommand used:

- **USAGE**: Returns an integer representing the memory usage in bytes.
- **STATS**: Returns a nested array of statistics about memory usage.
- **PURGE**: Returns 'OK' when the operation is successful.
- **MALLOC-STATS**: Returns a bulk string with detailed memory allocator stats.
- **HELP**: Returns an array of strings describing each subcommand.

## Code Examples

Showing examples using CLI with the `dragonfly>` prompt:

```cli
dragonfly> MEMORY USAGE mykey
(integer) 56

dragonfly> MEMORY STATS
1) "peak.allocated"
2) (integer) 8388608
3) "total.allocated"
4) (integer) 6250000
5) "startup.allocated"
6) (integer) 1000000
7) "replication.backlog"
8) (integer) 1048576
9) "clients.slaves"
10) (integer) 20480
11) "clients.normal"
12) (integer) 102400
13) "aof.buffer"
14) (integer) 0
15) "lua.caches"
16) (integer) 0
17) "functions.caches"
18) (integer) 0
19) "overhead.total"
20) (integer) 524288
21) "keys.count"
22) (integer) 1000
23) "keys.bytes-per-key"
24) (integer) 16
25) "dataset.bytes"
26) (integer) 2097152
27) "dataset.percentage"
28) "33.33%"
29) "peak.percentage"
30) "75.00%"

dragonfly> MEMORY PURGE
"OK"

dragonfly> MEMORY MALLOC-STATS
"___ Begin jemalloc statistics ___\nAllocated: 8388608, active: 12582912, metadata: 4194304...\n___ End jemalloc statistics ___"

dragonfly> MEMORY HELP
1) "MEMORY DOCTOR"
2) "MEMORY USAGE <key>"
3) "MEMORY STATS"
4) "MEMORY PURGE"
5) "MEMORY MALLOC-STATS"
6) "MEMORY HELP"
```

## Best Practices

- Regularly monitor your memory usage with `MEMORY STATS` to prevent out-of-memory errors.
- Use `MEMORY PURGE` cautiously; it's helpful for freeing up memory but can impact performance if overused.

## Common Mistakes

- Overlooking memory overhead: Remember that keys, clients, and other structures add significant overhead beyond just the raw data stored.
- Misinterpreting output: Ensure you understand the units and metrics reported by commands like `MEMORY USAGE`.

## FAQs

### What does `MEMORY USAGE` actually measure?

`MEMORY USAGE` reports the memory used by the specified key, including associated metadata.

### How often should I run `MEMORY STATS`?

Running `MEMORY STATS` periodically (e.g., every few minutes) can help you stay informed about your Redis instance's memory health without causing significant overhead.
