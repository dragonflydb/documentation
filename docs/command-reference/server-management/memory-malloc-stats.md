---
description: Learn how to use Redis MEMORY MALLOC-STATS command to retrieve memory allocator stats.
---

import PageTitle from '@site/src/components/PageTitle';

# MEMORY MALLOC-STATS

<PageTitle title="Redis MEMORY MALLOC-STATS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`MEMORY MALLOC-STATS` is a debugging command in Redis used to display internal statistics from the memory allocator. This command provides detailed information about memory usage patterns, which can be invaluable for diagnosing memory fragmentation issues and optimizing memory usage in Redis instances.

## Syntax

```
MEMORY MALLOC-STATS
```

## Parameter Explanations

`MEMORY MALLOC-STATS` does not take any parameters.

## Return Values

The command returns a bulk string with details about the memory allocator's internal state. The output is typically extensive and includes various metrics related to memory allocation and usage.

### Example Output

```text
___ Begin jemalloc statistics ___
Version: 5.1.0-0-g4e8a9e104889e7e0906cde300e2b313dd843d1e7
Assertions enabled
Run-time option settings:
  opt.abort: false
  opt.lg_chunk: 21
...
Allocated: 8388608, active: 9437184, metadata: 118784, resident: 9961472, mapped: 100663296, retained: 0
___ End jemalloc statistics ___
```

## Code Examples

```cli
dragonfly> MEMORY MALLOC-STATS
"___ Begin jemalloc statistics ___\nVersion: 5.1.0-0-g4e8a9e104889e7e0906cde300e2b313dd843d1e7\nAssertions enabled\nRun-time option settings:\n  opt.abort: false\n  opt.lg_chunk: 21\n...\nAllocated: 8388608, active: 9437184, metadata: 118784, resident: 9961472, mapped: 100663296, retained: 0\n___ End jemalloc statistics ___"
```

## Best Practices

- Use `MEMORY MALLOC-STATS` primarily in development or staging environments where you can safely analyze and act upon the detailed memory statistics without impacting production stability.
- Combine this command with other memory-related commands like `INFO memory` for a comprehensive understanding of your Redis instance's memory usage.

## Common Mistakes

- Avoid running `MEMORY MALLOC-STATS` frequently in production as the data returned can be verbose and may slightly affect performance due to the overhead in generating the statistics.

## FAQs

### What is the main use of `MEMORY MALLOC-STATS`?

`MEMORY MALLOC-STATS` is mainly used for debugging purposes to understand how the memory allocator in Redis is managing memory, useful for diagnosing memory fragmentation or leaks.

### Can `MEMORY MALLOC-STATS` be used in all versions of Redis?

No, this command is specific to Redis versions that use the Jemalloc allocator, which is generally the default allocator for Redis.
