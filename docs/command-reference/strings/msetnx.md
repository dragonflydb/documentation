---
description: Understand how to use Redis MSETNX to set multiple keys only if they don't exist.
---

import PageTitle from '@site/src/components/PageTitle';

# MSETNX

<PageTitle title="Redis MSETNX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `MSETNX` command is used to set multiple keys to multiple values, but only if none of the keys already exist.
It stands for "**Multi-Set if Not Exists**" and ensures atomicity—you can set multiple key-value pairs only when none of the keys are currently set in the database.

This command is particularly useful in scenarios where you need to initialize several keys at once in an atomic fashion but want to ensure no overwriting of existing keys.

## Syntax

```shell
MSETNX key1 value1 [key2 value2 ...]
```

- **Time complexity:** O(N) where N is the number of keys to set.
- **ACL categories:** @write, @string, @slow

## Parameter Explanations

- `key1`, `key2`, ...: The names of the keys whose values you are setting.
- `value1`, `value2`, ...: The values you want to associate with the respective keys.

## Return Values

The command returns:

- `(integer) 1`: if all keys were successfully set.
- `(integer) 0`: if no keys were set because at least one key already exists.

## Code Examples

### Basic Example

Set multiple keys only if none of them exist:

```shell
dragonfly> MSETNX user:1000 "Alice" user:1001 "Bob"
(integer) 1  # Both keys were set because they didn't exist before.
dragonfly> MGET user:1000 user:1001
1) "Alice"
2) "Bob"
```

### Example When a Key Exists

If at least one of the keys exists, no keys are set:

```shell
dragonfly> SET user:1002 "Charlie"
OK
dragonfly> MSETNX user:1000 "Alice" user:1002 "Dave"
(integer) 0  # No keys were set because "user:1002" already exists.
dragonfly> MGET user:1000 user:1002
1) (nil)     # "user:1000" wasn't set.
2) "Charlie" # "user:1002" remains unchanged.
```

### Using `MSETNX` in a Locking Mechanism

`MSETNX` can be used to implement simple resource locking, ensuring nobody else can claim the resource while it's in use:

```shell
# Acquiring a distributed lock for resource:lock
dragonfly> MSETNX resource:lock "locked"
(integer) 1  # Lock acquired.

# Another process trying to acquire the same lock
dragonfly> MSETNX resource:lock "locked"
(integer) 0  # Lock was not acquired since it's already held.

# Releasing the lock (using DEL)
dragonfly> DEL resource:lock
(integer) 1  # Lock released.
```

## Best Practices

- `MSETNX` ensures atomicity, so leverage it when you need to change or initialize several keys at once without risk of partial updates.
- Use it for tasks like session management, distributed locking, or maintaining idempotency where creation should only occur if all related data is absent.

## Common Mistakes

- Using `MSETNX` when you need to overwrite existing values.
  If you intend to overwrite, you should use `MSET` instead.
- Expecting the command to set only non-existent keys, even if some already exist.
  `MSETNX` sets no keys if even **one existing key** is detected.

## FAQs

### What happens if none of the keys exist?

If none of the keys exist, `MSETNX` will successfully set all keys and return `(integer) 1`.

### Will `MSETNX` overwrite an existing key?

No, `MSETNX` will not overwrite any key.
If any key already exists, the command does **nothing**, and none of the keys are set.

### Can I use `MSETNX` with multiple databases?

`MSETNX`, like other commands, operates within the context of the currently selected database.
To use it across multiple databases, you'd need to switch between databases and apply the command separately.
