---
description: Learn how to use Redis FLUSHDB command to remove all keys from the current database.
---

import PageTitle from '@site/src/components/PageTitle';

# FLUSHDB

<PageTitle title="Redis FLUSHDB Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`FLUSHDB` is a Redis command used to remove all keys from the current database. This command is typically used in scenarios where you need to clear out an entire Redis database, such as during testing, development, or when resetting environments.

## Syntax

```plaintext
FLUSHDB [ASYNC]
```

## Parameter Explanations

- `ASYNC`: (Optional) If specified, the database will be cleared asynchronously, allowing the server to continue processing other commands while the deletion is in progress.

## Return Values

The return value of the `FLUSHDB` command is a simple string reply indicating the success of the operation.

Example outputs:

- Without `ASYNC`:
  ```plaintext
  OK
  ```
- With `ASYNC`:
  ```plaintext
  OK
  ```

## Code Examples

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> KEYS *
1) "key1"
2) "key2"
dragonfly> FLUSHDB
OK
dragonfly> KEYS *
(empty list or set)
```

Using `ASYNC`:

```cli
dragonfly> SET key1 "value1"
OK
dragonfly> SET key2 "value2"
OK
dragonfly> FLUSHDB ASYNC
OK
dragonfly> KEYS *
(empty list or set)
```

## Best Practices

- Use `FLUSHDB` cautiously in production environments, as it will irreversibly delete all keys in the current database.
- Consider using `FLUSHDB ASYNC` for larger datasets to avoid blocking the Redis server.

## Common Mistakes

- Using `FLUSHDB` without realizing it clears only the current database, not all databases. To clear all databases, use `FLUSHALL`.
- Forgetting that `ASYNC` does not guarantee immediate deletion but allows the server to handle other operations concurrently.

## FAQs

### Is there a way to recover data after using FLUSHDB?

No, once `FLUSHDB` is executed, the action is irreversible, and all data in the current database is permanently deleted. Always ensure you have backups if needed.

### Does FLUSHDB affect other databases in Redis?

No, `FLUSHDB` only removes keys from the currently selected database. Other databases in the same Redis instance remain unaffected.
