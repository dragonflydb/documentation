---
description: Learn how to use Redis PSETEX to set key's value and expiration in milliseconds.
---

import PageTitle from '@site/src/components/PageTitle';

# PSETEX

<PageTitle title="Redis PSETEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PSETEX` command in Redis sets the value of a key and specifies a time-to-live (TTL) for the key in milliseconds. It's typically used when you need to store temporary data that should expire after a precise duration.

## Syntax

```
PSETEX key milliseconds value
```

## Parameter Explanations

- **key**: The name of the key where the value will be set.
- **milliseconds**: The TTL for the key in milliseconds. After this period, the key will automatically be deleted.
- **value**: The value to be stored in the key.

## Return Values

- **OK**: If the operation is successful.

Example:

```cli
dragonfly> PSETEX mykey 1000 "Hello, World!"
"OK"
```

## Code Examples

Setting a key with `PSETEX` and verifying its expiration:

```cli
dragonfly> PSETEX mykey 5000 "temporary_value"
"OK"
dragonfly> GET mykey
"temporary_value"
# Wait for 5 seconds
dragonfly> GET mykey
(nil)
```

## Best Practices

- Use `PSETEX` when you need operations with millisecond precision for TTLs.
- Ensure that your application logic accounts for the possible expiry of keys.

## Common Mistakes

- Providing an invalid TTL value (e.g., non-integer or negative values).
- Expecting the key to persist without accounting for its expiration.

## FAQs

### What happens if I set a TTL of zero milliseconds?

If you set a TTL of zero milliseconds, the key will be instantly expired and deleted.

### Can I update the TTL of an existing key with `PSETEX`?

No, `PSETEX` sets both the value and TTL at once. To update the TTL of an existing key, use the `PEXPIRE` command.
