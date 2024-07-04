---
description: Learn how to use Redis SETNX for setting a key's value, only if the key does not exist.
---

import PageTitle from '@site/src/components/PageTitle';

# SETNX

<PageTitle title="Redis SETNX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SETNX` command in Redis sets a key to a specified value if the key does not already exist. This atomic operation is useful for implementing distributed locks or ensuring that a key is only set if it hasn't been set before.

## Syntax

```
SETNX key value
```

## Parameter Explanations

- **key**: The name of the key to be set.
- **value**: The value to associate with the key if it does not already exist.

## Return Values

- **1**: The key was set.
- **0**: The key was not set because it already exists.

## Code Examples

```cli
dragonfly> SETNX mykey "Hello"
(integer) 1
dragonfly> SETNX mykey "World"
(integer) 0
dragonfly> GET mykey
"Hello"
```

## Best Practices

When using `SETNX` to implement a lock, consider setting an expiration on the key using `EXPIRE` to avoid potential deadlocks if a client crashes while holding a lock.

## FAQs

### How can I use `SETNX` to implement a simple lock?

You can combine `SETNX` with `EXPIRE` to create a basic locking mechanism. For example:

```cli
dragonfly> SETNX lock_key "lock_value"
(integer) 1
dragonfly> EXPIRE lock_key 10
(integer) 1
```

This ensures that the lock will automatically expire after 10 seconds if not released.

### What happens if I call `SETNX` on an existing key?

If the key already exists, `SETNX` will return 0 and will not modify the key's value.
