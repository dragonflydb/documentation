---
description: "Understand the use of Redis PEXPIRE command to set key expiry in milliseconds."
---

import PageTitle from '@site/src/components/PageTitle';

# PEXPIRE

<PageTitle title="Redis PEXPIRE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PEXPIRE` command in Redis is used to set a timeout on a key with a specified expiration time in milliseconds. This is useful for scenarios where you need more granular control over expiration times than the second granularity provided by the `EXPIRE` command. Typical use cases include caching mechanisms, session management, and temporary data storage.

## Syntax

```
PEXPIRE key milliseconds
```

## Parameter Explanations

- **key**: The name of the key you want to set the expiration time for.
- **milliseconds**: The expiration time in milliseconds. This value must be a positive integer.

## Return Values

The `PEXPIRE` command returns an integer indicating whether the timeout was successfully set:

- `(integer) 1`: The timeout was set successfully.
- `(integer) 0`: The key does not exist or the timeout could not be set.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> PEXPIRE mykey 1500
(integer) 1
dragonfly> TTL mykey
(integer) 1
dragonfly> PTTL mykey
(integer) 1499
dragonfly> GET mykey
(nil)  // After 1.5 seconds, the key will expire
```

## Best Practices

- Use `PEXPIRE` when you need millisecond precision for key expiration.
- Combine with other commands like `SET` to ensure keys have both a value and expiration time in atomic operations (e.g., using `SET key value PX milliseconds`).

## Common Mistakes

- Setting a negative or zero value for the `milliseconds` parameter will result in an error.
- Forgetting that the key must exist for `PEXPIRE` to work; otherwise, it returns `(integer) 0`.

## FAQs

### What happens if I try to set a PEXPIRE on a non-existent key?

If the key does not exist, `PEXPIRE` will return `(integer) 0`.

### Can I remove an expiration timeout once set with PEXPIRE?

Yes, you can remove the expiration timeout using the `PERSIST` command.
