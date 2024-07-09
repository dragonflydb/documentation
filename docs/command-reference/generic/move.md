---
description: "Learn usage of Redis MOVE command that moves a key to another database."
---

import PageTitle from '@site/src/components/PageTitle';

# MOVE

<PageTitle title="Redis MOVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `MOVE` command in Redis is used to transfer a key from the current database to a specified destination database. This is particularly useful for organizing data across different databases within the same Redis instance, allowing for separation of concerns or staged processing.

Typical use cases include:

- Migrating keys between different databases for load balancing.
- Staging data in intermediate databases before moving it to a production database.

## Syntax

```plaintext
MOVE key db
```

## Parameter Explanations

- `key`: The key to be moved. This must exist in the current database for the operation to succeed.
- `db`: The target database number where the key should be moved. It must be an integer and refer to an existing Redis database.

## Return Values

- `(integer) 1`: Indicates that the key was successfully moved to the target database.
- `(integer) 0`: Indicates failure, either because the key does not exist in the current database or it already exists in the target database.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> MOVE mykey 1
(integer) 1
dragonfly> EXISTS mykey
(integer) 0
dragonfly> SELECT 1
OK
dragonfly> EXISTS mykey
(integer) 1
dragonfly> GET mykey
"Hello"
dragonfly> MOVE mykey 0
(integer) 1
dragonfly> SELECT 0
OK
dragonfly> GET mykey
"Hello"
```

## Best Practices

- Ensure that the target database is ready to receive the key to avoid accidentally overwriting data.
- Regularly verify the existence of keys in both source and target databases after performing the move operation.

## Common Mistakes

- Attempting to move a non-existent key, which results in no action while returning `(integer) 0`.
- Overwriting an existing key in the target database. The `MOVE` command will fail if the key already exists in the target database, so check for key existence beforehand if needed.

## FAQs

### What happens if the key already exists in the target database?

If the key already exists in the destination database, the `MOVE` command will not overwrite it and will return `(integer) 0`.

### Can I move multiple keys at once using the MOVE command?

No, the `MOVE` command only supports moving one key at a time. To move multiple keys, you need to call the `MOVE` command separately for each key.
