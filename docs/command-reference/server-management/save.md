---
description: Learn how to use Redis SAVE command to create a backup of the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# SAVE

<PageTitle title="Redis SAVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SAVE` command in Redis is used to synchronously save the dataset to disk. This command is particularly useful in scenarios where you need to ensure that all changes to your dataset are persisted immediately, such as before a planned maintenance window or shutdown.

## Syntax

```plaintext
SAVE
```

## Parameter Explanations

The `SAVE` command does not take any parameters. It simply forces a synchronous save of the dataset.

## Return Values

- **OK**: If the save operation was successful.
- **Error**: If the save operation failed for some reason (e.g., during an ongoing save).

## Code Examples

```cli
dragonfly> SAVE
OK
```

## Best Practices

- Use `SAVE` sparingly in production environments because it blocks the server until the save operation completes, which can affect performance and availability.
- For regular backups, consider using `BGSAVE`, which performs the save operation in the background without blocking.

## Common Mistakes

- Using `SAVE` in a high-load production environment can lead to significant latency due to its blocking nature. Always prefer `BGSAVE` unless absolutely necessary.
- Assuming `SAVE` guarantees no data loss; while it does persist data immediately, unexpected failures right after the save could still pose risks.

## FAQs

### What is the difference between SAVE and BGSAVE?

`SAVE` performs a synchronous save and blocks the Redis server until the operation completes. `BGSAVE` performs the save in the background, allowing the server to continue processing other commands.

### Can I use SAVE in a script?

Yes, but be aware that it will block the entire Redis server during the execution, potentially causing high latency for other operations.
