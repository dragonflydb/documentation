---
description: Learn how to use Redis CONFIG SET command to set the configuration of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG SET

<PageTitle title="Redis CONFIG SET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`CONFIG SET` is a command in Redis used to alter the configuration of a running Redis server without restarting it. This command is typically used for tuning performance, changing logging levels, or modifying any other operational parameters dynamically. Common scenarios include adjusting memory limits, enabling/disabling features, and changing replication settings on the fly.

## Syntax

```
CONFIG SET <parameter> <value>
```

## Parameter Explanations

- `<parameter>`: The name of the configuration parameter you want to set. For instance, `maxmemory`, `loglevel`, etc.
- `<value>`: The new value for the specified configuration parameter. This could be an integer, string, or boolean, depending on the parameter.

## Return Values

The `CONFIG SET` command returns a simple string reply:

- `OK`: If the configuration was successfully updated.
- An error message: If the parameter name is invalid or the value is out of acceptable range/types.

## Code Examples

```cli
dragonfly> CONFIG SET maxmemory 512mb
OK
dragonfly> CONFIG SET loglevel debug
OK
dragonfly> CONFIG SET appendonly yes
OK
```

## Best Practices

- Only change configurations that you fully understand as improper values can lead to instability.
- Test configuration changes on a non-production instance before applying them to your production Redis server.
- Use `CONFIG GET` to check current values before making changes with `CONFIG SET`.

## Common Mistakes

- Setting inappropriate values that exceed system resources (e.g., setting `maxmemory` higher than available RAM).
- Forgetting to persist changes if needed. Some configurations might revert after a restart unless saved in the Redis configuration file.

## FAQs

### What happens if I set an invalid parameter?

Redis will return an error indicating that the parameter is not recognized or the value is invalid.

### Does `CONFIG SET` affect all connected clients immediately?

Yes, changes made using `CONFIG SET` apply globally and take effect immediately, impacting all connected clients.

### Is it possible to reset a configuration to its default value?

You need to either set the parameter to its default value using `CONFIG SET` or modify the Redis configuration file and restart the server.
