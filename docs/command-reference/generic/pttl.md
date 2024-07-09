---
description: "Learn to apply Redis PTTL command to get the time-to-live of a key in milliseconds."
---

import PageTitle from '@site/src/components/PageTitle';

# PTTL

<PageTitle title="Redis PTTL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PTTL` command in Redis is used to retrieve the remaining time to live (TTL) for a key in milliseconds. This command is useful when you need to know how much longer a key will exist before it expires, which can help in cache management and data lifecycle control.

## Syntax

```plaintext
PTTL key
```

## Parameter Explanations

- **key**: The name of the key whose TTL you are querying. It should be a string representing the key in the Redis database.

## Return Values

- **integer**: If the key exists and has an associated expiration time, the command returns the TTL in milliseconds.
- **-1**: If the key exists but has no associated expiration time.
- **-2**: If the key does not exist.

## Code Examples

```cli
dragonfly> SETEX mykey 5 "Hello"
OK
dragonfly> PTTL mykey
(integer) 4999
dragonfly> PTTL mynonexistentkey
(integer) -2
dragonfly> SET mynewkey "World"
OK
dragonfly> PTTL mynewkey
(integer) -1
```

## Best Practices

- Use `PTTL` over `TTL` when you need more precise information about the expiration time in milliseconds.
- Regularly monitor keys with expiration to manage and optimize cache performance efficiently.

## Common Mistakes

- Using `PTTL` on keys that do not exist or have no expiration set often results in confusion. Always check the return values carefully (-1 and -2) to handle such cases gracefully.

## FAQs

### What is the difference between TTL and PTTL?

`TTL` returns the remaining time to live of a key in seconds, while `PTTL` returns it in milliseconds, providing higher precision.

### Can I use PTTL on all types of keys?

Yes, `PTTL` works with any key type, but the key must exist and have an expiration set to return a positive value.

### What happens if I query PTTL on a persistent key?

If the key exists but does not have an expiration set, `PTTL` will return -1.
