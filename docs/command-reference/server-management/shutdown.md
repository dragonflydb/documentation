---
description: Learn how to use Redis SHUTDOWN command which terminates the server securely.
---

import PageTitle from '@site/src/components/PageTitle';

# SHUTDOWN

<PageTitle title="Redis SHUTDOWN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SHUTDOWN` command is used to stop the Redis server. It ensures that all data is saved to disk before shutting down, making it useful for maintenance or when gracefully rebooting the server. Typical scenarios include scheduled maintenance, configuration changes requiring a restart, or controlled server shutdowns.

## Syntax

```cli
SHUTDOWN [NOSAVE|SAVE]
```

## Parameter Explanations

- **NOSAVE**: Instructs Redis to shut down without saving the current dataset to disk.
- **SAVE**: Forces Redis to perform a synchronous save operation before shutting down. This is the default behavior if no parameters are provided.

## Return Values

This command does not return any values as the server stops processing commands immediately upon execution.

## Code Examples

```cli
dragonfly> SHUTDOWN
# No output as the server shuts down

dragonfly> SHUTDOWN NOSAVE
# No output as the server shuts down without saving data

dragonfly> SHUTDOWN SAVE
# No output as the server performs a save then shuts down
```

## Best Practices

1. **Ensure Data Persistence**: Always use `SHUTDOWN SAVE` unless you are certain that an explicit save is unnecessary.
2. **Graceful Shutdown**: Prefer the `SHUTDOWN` command over terminating the process forcefully to avoid potential data loss.

## Common Mistakes

- **Forgetting to Save Data**: Using `SHUTDOWN NOSAVE` when data persistence is required can result in data loss. Always assess whether an explicit save is necessary.

## FAQs

### What happens if I run `SHUTDOWN` without any parameters?

By default, running `SHUTDOWN` without parameters will perform a `SAVE` operation before shutting down the server.

### Can `SHUTDOWN` be called from within a script or application?

Yes, but be cautious as it will make Redis unavailable until it is restarted. Ensure this fits within your application's operational requirements.
