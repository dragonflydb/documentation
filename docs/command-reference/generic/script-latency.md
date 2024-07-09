---
description: "Get the Redis SCRIPT LATENCY command to manage script evaluation latency."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT LATENCY

<PageTitle title="Redis SCRIPT LATENCY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SCRIPT LATENCY` Redis command provides statistics about the latency of Lua scripts executed by the server. This command is useful for monitoring and optimizing the performance of scripts to ensure efficient execution. Typical scenarios include identifying bottlenecks in script execution, debugging slow scripts, and maintaining optimal performance in a high-load environment.

## Syntax

```plaintext
SCRIPT LATENCY [RESET]
```

## Parameter Explanations

- **RESET**: Optional. If provided, this parameter resets the collected latency statistics. Without this parameter, the command just returns the current statistics.

## Return Values

When `RESET` is not provided:

- The command returns an array with latency statistics of the scripts run.

Example output:

```plaintext
1)  (integer) total_calls
2)  (integer) total_time (in microseconds)
3)  (integer) max_time (in microseconds)
4)  (integer) min_time (in microseconds)
5)  (integer) avg_time (in microseconds)
```

When `RESET` is provided:

- The command returns a simple string reply:

```plaintext
"OK"
```

## Code Examples

```cli
dragonfly> SCRIPT LATENCY
1) (integer) 5
2) (integer) 15000
3) (integer) 5000
4) (integer) 2000
5) (integer) 3000
dragonfly> SCRIPT LATENCY RESET
"OK"
dragonfly> SCRIPT LATENCY
1) (integer) 0
2) (integer) 0
3) (integer) 0
4) (integer) 0
5) (integer) 0
```

## Best Practices

- Regularly monitor script latencies to identify and optimize slow scripts.
- Use the `SCRIPT LATENCY RESET` command to clear statistics periodically, especially after making changes to scripts, to get accurate performance data.

## Common Mistakes

- Ignoring latency statistics can lead to unoptimized scripts that degrade performance.
- Forgetting to reset the latency statistics can result in misleading data over time, especially if the scripts are frequently modified.

## FAQs

### How often should I reset the script latency statistics?

It’s advisable to reset latency statistics whenever significant changes are made to scripts or when starting a new performance monitoring cycle to ensure the data reflects the current state accurately.

### What does each item in the latency statistics array represent?

- **total_calls**: Number of times scripts have been called.
- **total_time**: Total time spent in executing scripts (in microseconds).
- **max_time**: Maximum execution time for a single script run (in microseconds).
- **min_time**: Minimum execution time for a single script run (in microseconds).
- **avg_time**: Average execution time per script run (in microseconds).
