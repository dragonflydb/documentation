---
description: Learn how to use Redis CONFIG command to configure Redis server at runtime.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG

<PageTitle title="Redis CONFIG Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `CONFIG` command in Redis is used to manage the server configuration at runtime without the need to restart the server. It allows administrators to view, set, and rewrite configuration parameters. Typical use cases include changing settings for logging, memory limits, or adjusting behavior during maintenance.

## Syntax

```plaintext
CONFIG GET <parameter>
CONFIG SET <parameter> <value>
CONFIG RESETSTAT
CONFIG REWRITE
```

## Parameter Explanations

- `<parameter>`: The name of the configuration parameter you want to get or set. For example, `loglevel`, `maxmemory`.
- `<value>`: The new value for the configuration parameter.

## Return Values

- `CONFIG GET <parameter>`: Returns a list of keys and their current values.

  Example:

  ```cli
  dragonfly> CONFIG GET loglevel
  1) "loglevel"
  2) "notice"
  ```

- `CONFIG SET <parameter> <value>`: Returns `OK` if the configuration change was successful.

  Example:

  ```cli
  dragonfly> CONFIG SET loglevel verbose
  OK
  ```

- `CONFIG RESETSTAT`: Resets the statistics reported by Redis.

  Example:

  ```cli
  dragonfly> CONFIG RESETSTAT
  OK
  ```

- `CONFIG REWRITE`: Rewrites the configuration file with the current configuration.

  Example:

  ```cli
  dragonfly> CONFIG REWRITE
  OK
  ```

## Code Examples

```cli
dragonfly> CONFIG GET maxmemory
1) "maxmemory"
2) "0"

dragonfly> CONFIG SET maxmemory 104857600
OK

dragonfly> CONFIG GET maxmemory
1) "maxmemory"
2) "104857600"

dragonfly> CONFIG RESETSTAT
OK

dragonfly> CONFIG REWRITE
OK
```

## Best Practices

- Use `CONFIG SET` cautiously as it can affect the stability and performance of your Redis instance.
- Always back up your current configuration before making changes.
- Apply changes during maintenance windows if possible to avoid impacting live traffic.

## Common Mistakes

- Setting inappropriate values that exceed the server's physical resources leading to crashes or slowdowns.
- Forgetting to perform `CONFIG REWRITE` after setting new configurations which results in the loss of changes after a restart.

## FAQs

### What happens if I don't use `CONFIG REWRITE` after `CONFIG SET`?

Without `CONFIG REWRITE`, the changes made using `CONFIG SET` are not saved to the configuration file and will be lost upon server restart.

### Can all configuration parameters be changed using `CONFIG SET`?

No, some parameters are read-only at runtime and cannot be changed using `CONFIG SET`.
