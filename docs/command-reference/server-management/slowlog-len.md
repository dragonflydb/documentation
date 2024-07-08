---
description: Discover how to use Redis SLOWLOG LEN command to retrieve the current number of entries in the slow log.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG LEN

<PageTitle title="Redis SLOWLOG LEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SLOWLOG LEN` command is part of the Redis Slow Log feature, used to inspect the length of the slow query log. This log records queries that exceed a certain execution time threshold, allowing administrators to identify and optimize inefficient commands. Typical scenarios include performance monitoring and debugging.

## Syntax

```cli
SLOWLOG LEN
```

## Parameter Explanations

This command does not take any parameters.

## Return Values

The `SLOWLOG LEN` command returns an integer representing the number of entries in the slow log.

### Example Outputs

- `(integer) 0`: No slow queries have been logged.
- `(integer) 5`: There are five entries in the slow log.

## Code Examples

```cli
dragonfly> SLOWLOG LEN
(integer) 3
```

## Best Practices

- Regularly monitor the slow log length to maintain optimal performance.
- Adjust the `slowlog-log-slower-than` configuration to define what qualifies as a slow query based on your specific needs.

## Common Mistakes

- Ignoring a high number of entries in the slow log, which may indicate underlying performance issues.

## FAQs

### How can I clear the slow log?

Use the `SLOWLOG RESET` command to clear the slow log.

### What defines a slow query in Redis?

A slow query exceeds the execution time threshold set by the `slowlog-log-slower-than` configuration parameter.
