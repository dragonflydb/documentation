---
description: "Understand how to use Redis DUMP command for returning a serialized version of stored value."
---

import PageTitle from '@site/src/components/PageTitle';

# DUMP

<PageTitle title="Redis DUMP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DUMP` command in Redis is used to serialize a given key and return the serialized value. This command is particularly useful for migrating data between different Redis instances or for creating backups. It helps in efficiently exporting Redis data without having to copy entire databases.

## Syntax

```plaintext
DUMP key
```

## Parameter Explanations

- **key**: The name of the key you want to serialize. It must be a valid key that exists in the Redis database.

## Return Values

The `DUMP` command returns a binary string representing the serialized value of the given key. If the key does not exist, it returns `nil`.

Example:

```plaintext
"\x00\xc0\x02\x06\x00\xfa"
```

If the key doesn't exist:

```plaintext
(nil)
```

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> DUMP mykey
"\x00\xc0\x03\x05\x00\xf9rU$\x8f\x1e\x1c"
dragonfly> DUMP non_existent_key
(nil)
```

## Best Practices

- Ensure the key you are serializing with `DUMP` exists to avoid unnecessary errors.
- When using `DUMP` for migration, pair it with the `RESTORE` command to reconstitute the key in the target Redis instance.

## Common Mistakes

- Using `DUMP` on a non-existent key will return `nil`, which may lead to confusion if not handled properly in scripts.

## FAQs

### Can I use `DUMP` to migrate data between different versions of Redis?

Yes, you can use `DUMP` to serialize data from one Redis instance and `RESTORE` to deserialize it into another instance, even if they are running different versions of Redis.

### Is the output of `DUMP` human-readable?

No, the output of `DUMP` is a binary string. It is meant to be used programmatically and not for direct reading by humans.
