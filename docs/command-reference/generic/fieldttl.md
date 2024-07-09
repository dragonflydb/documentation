---
description: "Learn the Dragonfly FIELDTTL command to get remaining time-to-live of a key."
---

import PageTitle from '@site/src/components/PageTitle';

# FIELDTTL

<PageTitle title="Redis TTL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`FIELDTTL` is a command used in Redis to retrieve the remaining time to live (TTL) for a specific field within a hash. It is particularly useful when dealing with expiring data fields in use cases such as caching, session management, and temporary data storage.

## Syntax

```plaintext
FIELDTTL key field
```

## Parameter Explanations

- `key`: The key of the hash containing the field.
- `field`: The specific field within the hash for which to retrieve the TTL.

## Return Values

The command returns the time to live (in seconds) for the specified field. If the field does not exist or has no associated TTL, it returns -2. If the key does not exist, it returns -1.

Examples:

- Integer indicating TTL in seconds, e.g., `(integer) 120`
- `-2` if the field does not exist or has no TTL.
- `-1` if the key does not exist.

## Code Examples

```cli
dragonfly> HSET myhash field1 "value1"
(integer) 1
dragonfly> EXPIREFIELD myhash field1 3600
(integer) 1
dragonfly> FIELDTTL myhash field1
(integer) 3600
dragonfly> FIELDTTL myhash nonexistingfield
(integer) -2
dragonfly> FIELDTTL nonexistingkey field1
(integer) -1
```

## Best Practices

- Always check the return value of `FIELDTTL` to handle cases where the field or key might not exist.
- Use `FIELDTTL` in conjunction with `EXPIREFIELD` to manage field-specific TTLs effectively in your applications.

## Common Mistakes

- Forgetting that `FIELDTTL` only works on fields within hashes, not on the keys themselves.
- Misinterpreting the return value `-2` as indicating that the key does not exist when it actually means the field does not exist or has no TTL.

## FAQs

### Can I use `FIELDTTL` on a string or list?

No, `FIELDTTL` is specifically designed for fields within a hash. Use appropriate TTL commands like `TTL` for keys.

### What happens if I set a TTL on a field that doesn't exist?

Setting a TTL on a non-existing field will create the field and set its TTL if the corresponding command supports it.
