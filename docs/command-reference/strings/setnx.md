---
description: Learn how to use Redis SETNX for setting a key's value, only if the key does not exist.
---

import PageTitle from '@site/src/components/PageTitle';

# SETNX

<PageTitle title="Redis SETNX Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `SETNX` command is used to set a key to a specific value only if the key does not already exist.
It is primarily useful in scenarios involving distributed locking, or to ensure certain operations occur exactly once by multiple clients.
The combination of the **atomic nature of the command ensures that race conditions are prevented when multiple clients attempt to create the same key at the same time**.
Also note that the `SETNX` command can be replaced by the [`SET`](set.md) command with its `NX` option.

## Syntax

```shell
SETNX key value
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key to be set if it doesn't already exist.
- `value`: The value to associate with the key if the key is newly created.

## Return Values

- The command returns `1` if the key was set.
- It returns `0` if the key already exists.

## Code Examples

### Basic Example

Set a new key if it doesn't exist:

```shell
dragonfly$> SETNX mykey "hello"
(integer) 1
```

In this example, `"mykey"` did not exist, so the command sets it to `"hello"` and returns `1`.

### Attempt to Set an Existing Key

Attempt to set a key that already exists:

```shell
dragonfly$> SETNX mykey "world"
(integer) 0
```

Here, the key `"mykey"` already exists, so the value `"world"` is not set, and the command returns `0`.

### Using `SETNX` in Distributed Locking

One typical use case for `SETNX` is implementing a distributed lock.
The lock is created by setting a key if it doesn't already exist, preventing other clients from acquiring the lock.

```shell
dragonfly$> SETNX lock:resource "lock_token_1"
(integer) 1  # Lock acquired
```

If another client tries to acquire the lock, they would fail:

```shell
dragonfly$> SETNX lock:resource "lock_token_2"
(integer) 0  # Lock already held
```

## Best Practices

- Use `SETNX` when you want to ensure that an operation is executed only once.
  For example, you could use it to ensure an initialization routine runs only once even if multiple clients are attempting it.
- As part of distributed locking mechanisms, combine `SETNX` with `EXPIRE` to avoid deadlocks by ensuring timeouts on locks.
  However, it is recommended to use the [`SET`](set.md) command with its `NX` and `EX` options to perform both operations atomically.
  Moreover, consider using a library that implements [Redlock](../../integrations/redlock.md) or similar algorithms for distributed locking.

## Common Mistakes

- Forgetting that `SETNX` does **not** modify the value if the key exists.
- Relying on `SETNX` alone for locking mechanisms without a timeout can lead to deadlocks if a client holding a lock crashes or loses connection without releasing it.

## FAQs

### What happens if the key already exists?

If the key already exists, `SETNX` simply returns `0` and does not modify the key's value.

### Can I use `EXPIRE` with `SETNX`?

Yes, while `SETNX` itself does not provide an expiration feature,
you can execute a combination of `SETNX` and `EXPIRE` to ensure the key is set with a timeout, which is particularly useful for locking mechanisms.
However, prefer using the [`SET`](set.md) command with its `NX` and `EX` options or a library that implements distributed locking mechanisms.

```shell
dragonfly$> SETNX mylock "locked"
(integer) 1
dragonfly$> EXPIRE mylock 10  # Lock expires after 10 seconds
(integer) 1
```

### Can `SETNX` be used to check if a key exists without modifying it?

No, `SETNX` will attempt to set the key if it doesn't exist.
If you need to check if a key exists without setting it, use the [`EXISTS`](../generic/exists.md) command instead.
