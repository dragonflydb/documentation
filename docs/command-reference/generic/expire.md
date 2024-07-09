---
description: "Learn Redis EXPIRE command that sets a key's time-to-live in seconds."
---

import PageTitle from '@site/src/components/PageTitle';

# EXPIRE

<PageTitle title="Redis EXPIRE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `EXPIRE` command in Redis sets a timeout on a specified key. When the timeout expires, the key will be automatically deleted. This is commonly used in scenarios where data should only be available for a limited period, such as caching, session management, or temporary data storage.

## Syntax

```cli
EXPIRE key seconds
```

## Parameter Explanations

- `key`: The name of the key you want to set an expiration on.
- `seconds`: The time to live (TTL) for the key, specified in seconds. After this period, the key is automatically removed.

## Return Values

The `EXPIRE` command returns an integer:

- `1` if the timeout was successfully set.
- `0` if the key does not exist or the timeout could not be set.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
"OK"
dragonfly> EXPIRE mykey 10
(integer) 1
dragonfly> TTL mykey
(integer) 10
dragonfly> EXISTS mykey
(integer) 1
// Wait for more than 10 seconds
dragonfly> EXISTS mykey
(integer) 0
```

## Best Practices

- Use the `EXPIRE` command in conjunction with `SET` for creating keys that should automatically expire.
- Combine `EXPIRE` with `PERSIST` to remove the expiration from a key if needed.

## Common Mistakes

- Setting an expiration on non-existent keys results in a return value of `0`, which can lead to unexpected behavior if not checked properly.
- Confusing the units: `EXPIRE` uses seconds, whereas `PEXPIRE` uses milliseconds.

## FAQs

### What happens if I set a new expiry on a key that already has an expiry?

Setting a new expiration time on a key overrides the existing expiration time.

### Can I remove the expiration from a key?

Yes, use the `PERSIST` command to remove the expiration from a key.

### Will `EXPIRE` work on all data types in Redis?

`EXPIRE` works on any type of key, including strings, lists, sets, hashes, etc.
