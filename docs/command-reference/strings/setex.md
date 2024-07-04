---
description: Discover how to use Redis SETEX for setting key-value pairs with an expiration time.
---

import PageTitle from '@site/src/components/PageTitle';

# SETEX

<PageTitle title="Redis SETEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SETEX` command in Redis sets the value of a key with an expiration time. This is useful for caching data that should expire after a certain period, such as session tokens or temporary data.

## Syntax

```cli
SETEX key seconds value
```

## Parameter Explanations

- `key`: The name of the key you want to set.
- `seconds`: The expiration time for the key, specified in seconds.
- `value`: The value to associate with the key.

## Return Values

- **OK**: If the operation is successful.

## Code Examples

```cli
dragonfly> SETEX mykey 60 "example"
OK
dragonfly> GET mykey
"example"
dragonfly> TTL mykey
(integer) 59
```

## Best Practices

- Use `SETEX` for setting keys that need an automatic expiration, like session identifiers or temporary caches.
- Choose an appropriate expiration time based on your use case to avoid premature deletion or stale data lingering.

## Common Mistakes

- Setting the expiration time too short, causing the key to expire before it can be used.
- Forgetting that the expiration time is in seconds, leading to confusion with other time units.

## FAQs

### What happens if I call `SETEX` on an existing key?

Calling `SETEX` on an existing key will overwrite its value and reset its expiration time.

### Can I change the expiration time of a key without changing its value?

No, `SETEX` sets both the value and the expiration. To change only the expiration, use the `EXPIRE` or `PEXPIRE` commands.
