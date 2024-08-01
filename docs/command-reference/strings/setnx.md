---
description: Learn how to use Redis SETNX for setting a key's value, only if the key does not exist.
---

import PageTitle from '@site/src/components/PageTitle';

# SETNX

<PageTitle title="Redis SETNX Explained (Better Than Official Docs)" />

## Introduction

The `SETNX` command in Redis sets the value of a key, but only if the key does not already exist. This atomic operation is useful for scenarios where you want to ensure that a key is set exactly once, such as initializing a counter or setting up a lock.

## Syntax

```plaintext
SETNX key value
```

## Parameter Explanations

- **key**: The name of the key to set. Must be a string.
- **value**: The value to set for the key. Can be any string.

## Return Values

- **1**: If the key was set successfully.
- **0**: If the key already exists and was not set.

## Code Examples

### Basic Example

```cli
dragonfly> SETNX mykey "Hello"
(integer) 1
dragonfly> SETNX mykey "World"
(integer) 0
dragonfly> GET mykey
"Hello"
```

### Distributed Lock

Setting a distributed lock using `SETNX`:

```cli
dragonfly> SETNX lock:my_resource "unique_identifier"
(integer) 1
# Simulate another client trying to acquire the same lock
dragonfly> SETNX lock:my_resource "another_identifier"
(integer) 0
```

### Ensuring Single Initialization

Initialize a counter only if it doesn't exist:

```cli
dragonfly> SETNX counter "0"
(integer) 1
# Increment the counter
dragonfly> INCR counter
(integer) 1
dragonfly> SETNX counter "100"
(integer) 0
dragonfly> GET counter
"1"
```

## Best Practices

- Use `SETNX` for implementing simple locks, but consider using higher-level constructs like Redlock for robust distributed locking.
- Combine `SETNX` with expiration commands (like `EXPIRE`) to prevent stale locks.

## Common Mistakes

- Not checking the return value of `SETNX`. Always verify whether the key was set.
- Overusing `SETNX` without understanding its limitations, especially in high-concurrency environments.

## FAQs

### Can I use SETNX to implement a distributed lock?

Yes, but it's recommended to use higher-level libraries like Redlock for more complex locking requirements.

### What happens if I use SETNX on an existing key?

The command returns `(integer) 0`, and the key's value remains unchanged.
