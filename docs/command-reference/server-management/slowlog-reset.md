---
description: Discover how to use Redis SLOWLOG RESET command to clear all the entries from the slow log.
---

import PageTitle from '@site/src/components/PageTitle';

# SLOWLOG RESET

<PageTitle title="Redis SLOWLOG RESET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`SLOWLOG RESET` is a Redis command used to reset the statistics of the slow log, effectively clearing all the logged entries. This can be particularly useful in scenarios where you want to start fresh with new monitoring data for performance tuning or troubleshooting.

## Syntax

```
SLOWLOG RESET
```

## Parameter Explanations

This command does not take any parameters. Its sole purpose is to clear the current slow log entries.

## Return Values

The `SLOWLOG RESET` command returns a simple status reply indicating the success of the operation.

Example output:

```
"OK"
```

## Code Examples

```cli
dragonfly> SLOWLOG GET
1) 1) (integer) 3
   2) (integer) 1620001111
   3) (integer) 1000
   4) 1) "SET"
      2) "key"
      3) "value"
dragonfly> SLOWLOG RESET
"OK"
dragonfly> SLOWLOG GET
(empty array)
```

## Best Practices

- Use `SLOWLOG RESET` during off-peak hours to avoid losing potentially valuable diagnostic data.
- Regularly monitor your slow logs and reset them only when necessary for performance analysis.

## Common Mistakes

- Resetting the slow log without first analyzing the collected data can result in lost opportunities for optimizing Redis performance.
- Frequent resetting can make it difficult to track long-term trends in slow commands.

## FAQs

### Does `SLOWLOG RESET` affect the current performance of Redis?

No, `SLOWLOG RESET` has minimal impact on performance as it simply clears the stored slow log entries without affecting other operations.

### Can I recover slow log entries after using `SLOWLOG RESET`?

No, once the slow log entries are cleared using `SLOWLOG RESET`, they cannot be recovered. Ensure that you have reviewed or saved the data if needed before performing the reset.
