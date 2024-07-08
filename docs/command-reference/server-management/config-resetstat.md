---
description: Learn how to use Redis CONFIG RESETSTAT command to reset statistics of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG RESETSTAT

<PageTitle title="Redis CONFIG RESETSTAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`CONFIG RESETSTAT` is a Redis command used to reset the stats reported by the INFO command. This includes resetting counters such as the number of commands processed, connections received, and more. It is typically used when you need to clear statistics for monitoring purposes, or before starting a new performance test to ensure you're working with clean data.

## Syntax

```cli
CONFIG RESETSTAT
```

## Parameter Explanations

This command does not take any parameters.

## Return Values

The `CONFIG RESETSTAT` command returns a simple status reply indicating that the operation was successful.

Example:

```
OK
```

## Code Examples

```cli
dragonfly> INFO
# Server
redis_version:6.2.1
...

# Stats
total_connections_received:5
total_commands_processed:10
...

dragonfly> CONFIG RESETSTAT
OK

dragonfly> INFO
# Server
redis_version:6.2.1
...

# Stats
total_connections_received:0
total_commands_processed:0
...
```

## Best Practices

- Use `CONFIG RESETSTAT` before running performance tests to start with a clean slate.
- Regularly reset statistics in long-running instances if you're using them for operational monitoring to keep the data relevant.

## Common Mistakes

- Forgetting that this command does not affect historical data outside of the current runtime statistics.

## FAQs

### Does `CONFIG RESETSTAT` affect all clients connected to the Redis server?

No, it only resets the internal statistics counters of the Redis server; it does not impact connected clients.

### Can I undo a `CONFIG RESETSTAT` command?

No, once the statistics are reset, they cannot be restored. Be cautious when using this command.
