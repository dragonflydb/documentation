---
description: "Learn the Redis TTL command to get remaining time-to-live of a key."
---

import PageTitle from '@site/src/components/PageTitle';

# TTL

<PageTitle title="Redis TTL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `TTL` command in Redis is used to determine the remaining time-to-live (in seconds) of a key that has an expiration set. This is useful for monitoring how long a key will persist before being automatically deleted, which can be critical in caching scenarios, session management, or any use case where automatic key expiration is required.

## Syntax

```plaintext
TTL <key>
```

## Parameter Explanations

- **key**: The name of the key for which you want to check the TTL. It must be a valid key that exists in the database and has an expiration set.

## Return Values

- An integer representing the time-to-live in seconds.
  - Returns the number of seconds until the key expires.
  - Returns `-1` if the key exists but has no associated expiration.
  - Returns `-2` if the key does not exist.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIRE mykey 10
(integer) 1
dragonfly> TTL mykey
(integer) 10
dragonfly> TTL mynonexistentkey
(integer) -2
dragonfly> SET anotherkey "World"
OK
dragonfly> TTL anotherkey
(integer) -1
```

## Best Practices

- Ensure keys that require expiration are always set with an expiry time using `EXPIRE`, `SETEX`, or other relevant commands.
- Regularly monitor TTLs to manage cache efficiency and avoid unexpected key evictions.

## Common Mistakes

- Forgetting to set an expiration on keys that should expire, leading to incorrect assumptions about their persistence.
- Misinterpreting the `-1` return value as an indication that the key does not exist, when it actually means the key exists without an expiration.

## FAQs

### What happens when a key with a TTL expires?

When a key's TTL reaches zero, Redis automatically deletes the key from the database.

### Can I change the TTL of an existing key?

Yes, you can use the `EXPIRE` command again on the key to reset its TTL.

### Is it possible to remove the TTL from a key?

Yes, using the `PERSIST` command on a key will remove its associated TTL, making it persistent.
