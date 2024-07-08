---
description: Learn how to use Redis BGSAVE command to create a backup of the database in background.
---

import PageTitle from '@site/src/components/PageTitle';

# BGSAVE

<PageTitle title="Redis BGSAVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BGSAVE` command in Redis is used to asynchronously save the dataset to disk. It's essential for creating backups, ensuring data durability, and can be used in conjunction with replication to keep slave instances in sync.

## Syntax

```plaintext
BGSAVE
```

## Parameter Explanations

The `BGSAVE` command does not take any parameters. It triggers an asynchronous background process that saves the current state of the database to a dump file.

## Return Values

- **Simple string reply**: Typically, `OK` if the background save started successfully.
- **Error reply**: If another save operation is already in progress or if the save could not be initiated due to some other issue.

## Code Examples

```cli
dragonfly> BGSAVE
"Background saving started"
dragonfly> BGSAVE
(error) ERR Background save already in progress
```

## Best Practices

- It's advisable to monitor the system's performance while using `BGSAVE`, especially on large datasets, as it can consume significant I/O resources.
- Combine `BGSAVE` with Redis replication to offload read traffic and distribute load.

## Common Mistakes

- Attempting to run multiple `BGSAVE` commands concurrently can lead to errors since only one background save operation can occur at a time.
- Not monitoring for errors or checking the status of the last background save can result in unnoticed data loss issues.

## FAQs

### What happens if the server crashes during a `BGSAVE`?

If the server crashes during a `BGSAVE`, the partial RDB file will be discarded and the existing RDB file remains unchanged. This ensures data integrity but may lead to a lack of recent changes in the backup.

### How can I check the status of a `BGSAVE` operation?

You can use the `LASTSAVE` command to get the Unix timestamp of the last successful save operation.

```cli
dragonfly> LASTSAVE
(integer) 1625651082
```

This indicates the last time the dataset was saved to disk successfully.
