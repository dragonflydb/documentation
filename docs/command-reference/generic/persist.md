---
description: "Learn how Redis PERSIST command removes a key's time-to-live."
---

import PageTitle from '@site/src/components/PageTitle';

# PERSIST

<PageTitle title="Redis PERSIST Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PERSIST` command in Redis is used to remove the expiration from a key, making it persistent. This is particularly useful when you have previously set a TTL (Time To Live) on a key but later decide that the key should exist indefinitely.

Typical scenarios include:

- Preserving user session data beyond its initial expiration.
- Retaining temporarily cached data for long-term use.

## Syntax

```plaintext
PERSIST key
```

## Parameter Explanations

- `key`: The name of the key for which you want to remove the expiration. It must be an existing key in your Redis instance.

## Return Values

- **(integer) 1**: If the timeout was successfully removed.
- **(integer) 0**: If the key does not exist or does not have an associated timeout.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIRE mykey 10
(integer) 1
dragonfly> PERSIST mykey
(integer) 1
dragonfly> TTL mykey
(integer) -1
dragonfly> PERSIST nonexistingkey
(integer) 0
```

## Best Practices

- Use `PERSIST` carefully as making certain keys persistent can lead to increased memory usage over time.
- Regularly audit your keys to ensure that only necessary keys are set to persist.

## Common Mistakes

- **Using PERSIST on non-existing keys**: This will always return 0. Ensure the key exists before calling `PERSIST`.
- **Assuming PERSIST sets a new expiration time**: `PERSIST` removes any existing expiration; it does not set a new one.

## FAQs

### What happens if I call PERSIST on a key without an expiration?

The command will return 0 since there is no timeout to remove.

### Can I use PERSIST on all types of keys?

Yes, `PERSIST` works with any type of key in Redis.
