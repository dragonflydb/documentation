---
description: "Use Redis PEXPIREAT command sets a key's time-to-live in UNIX time."
---

import PageTitle from '@site/src/components/PageTitle';

# PEXPIREAT

<PageTitle title="Redis PEXPIREAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PEXPIREAT` command in Redis is used to set the expiration time of a key in milliseconds, using an absolute Unix timestamp. This allows for precise control over when a key should expire. Typical use cases include setting timed cache items or implementing time-sensitive data invalidation.

## Syntax

```cli
PEXPIREAT key milliseconds-timestamp
```

## Parameter Explanations

- `key`: The name of the key you want to set an expiration for.
- `milliseconds-timestamp`: A Unix timestamp in milliseconds indicating the exact time at which the key will expire.

## Return Values

- `(integer) 1`: If the timeout was set successfully.
- `(integer) 0`: If the key does not exist or the timeout could not be set.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> PEXPIREAT mykey 1655100000000
(integer) 1
dragonfly> TTL mykey
(integer) 2592000
dragonfly> PEXPIREAT nonexistingkey 1655100000000
(integer) 0
```

## Best Practices

- Ensure that the Unix timestamp is accurate and correctly represents the intended expiration time.
- Use `PTTL` to verify the remaining time-to-live (TTL) of a key if needed.

## Common Mistakes

- Miscalculating the Unix timestamp in milliseconds can lead to unexpected expiration times.
- Using `PEXPIREAT` on a non-existent key will result in no operation, returning 0.

## FAQs

### How is `PEXPIREAT` different from `EXPIREAT`?

`PEXPIREAT` sets the expiration in milliseconds, allowing for more precise timing, whereas `EXPIREAT` sets it in seconds.

### Can I use `PEXPIREAT` to remove the expiration from a key?

No, `PEXPIREAT` only sets an expiration. To remove an expiration, use the `PERSIST` command.
