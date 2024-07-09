---
description: "Make use of Redis EXPIREAT command to set key expiry with UNIX timestamp."
---

import PageTitle from '@site/src/components/PageTitle';

# EXPIREAT

<PageTitle title="Redis EXPIREAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `EXPIREAT` command is used to set the expiration for a key as a UNIX timestamp. This means that at a specified date and time, the key will automatically be deleted from the database. This command is useful for scenarios where you need to ensure that data is only available until a specific point in time, such as session management, cache invalidation, or scheduling future deletions.

## Syntax

```cli
EXPIREAT key timestamp
```

## Parameter Explanations

- **key**: The key on which to set the expiration.
- **timestamp**: The UNIX timestamp (in seconds) indicating when the key should expire.

## Return Values

- Returns `(integer) 1` if the timeout was set successfully.
- Returns `(integer) 0` if the key does not exist or if the timeout could not be set.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> EXPIREAT mykey 1625097600
(integer) 1
dragonfly> TTL mykey
(integer) 1234567
dragonfly> EXPIREAT nonexistingkey 1625097600
(integer) 0
```

## Best Practices

- Ensure the timestamps you provide are accurate and account for differences in time zones if applicable.
- Use `TTL` to check how much time remains before a key expires.

## Common Mistakes

- Setting the timestamp in milliseconds instead of seconds can cause unexpected behavior.
- Trying to set expiration on a key that doesn't exist will always return 0 and have no effect.

## FAQs

### How can I convert a date and time to a UNIX timestamp?

You can use various programming languages or online tools to convert human-readable dates to UNIX timestamps. For example, in Python:

```python
import time
timestamp = int(time.mktime(time.strptime('2023-07-01 12:00:00', '%Y-%m-%d %H:%M:%S')))
print(timestamp)
```

### What happens if I set a new `EXPIREAT` on a key that already has an expiration?

Setting a new `EXPIREAT` on a key overwrites its existing expiration with the new timestamp.
