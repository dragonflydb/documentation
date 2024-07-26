---
description: Understand how to use Redis MSETNX to set multiple keys only if they don't exist.
---

import PageTitle from '@site/src/components/PageTitle';

# MSETNX

<PageTitle title="Redis MSETNX Explained (Better Than Official Docs)" />

## Introduction

The `MSETNX` command in Redis sets multiple keys to their respective values, but only if none of the keys already exist. This atomic operation ensures that either all keys are set or none are, preventing partial updates. It is particularly useful for scenarios where consistency and atomicity across multiple key-value pairs are required.

## Syntax

```plaintext
MSETNX key1 value1 [key2 value2 ...]
```

## Parameter Explanations

- `key1 value1`, `key2 value2`, ...: Pairs of keys and values to be set. All specified keys must not exist for the command to succeed.

## Return Values

- `(integer) 1`: Indicates that all keys were successfully set.
- `(integer) 0`: Indicates that no keys were set because at least one key already existed.

## Code Examples

### Basic Example

```cli
dragonfly> MSETNX key1 "value1" key2 "value2"
(integer) 1
dragonfly> MSETNX key3 "value3" key1 "newValue1"
(integer) 0
dragonfly> GET key1
"value1"
dragonfly> GET key2
"value2"
dragonfly> GET key3
(nil)
```

### Use Case: Ensuring Atomic Initialization

To atomically initialize configuration parameters if none have been set:

```cli
dragonfly> MSETNX config:host "localhost" config:port "6379"
(integer) 1
dragonfly> MSETNX config:host "127.0.0.1" config:port "6380"
(integer) 0
dragonfly> GET config:host
"localhost"
dragonfly> GET config:port
"6379"
```

### Use Case: Setting User Profile Defaults

Setting default values for a new user's profile if not already initialized:

```cli
dragonfly> MSETNX user:1001:name "John Doe" user:1001:email "john.doe@example.com"
(integer) 1
dragonfly> MSETNX user:1001:name "Jane Smith" user:1001:email "jane.smith@example.com"
(integer) 0
dragonfly> GET user:1001:name
"John Doe"
dragonfly> GET user:1001:email
"john.doe@example.com"
```

## Common Mistakes

### Ignoring Existing Keys

Assuming `MSETNX` will overwrite existing keys can lead to logical errors. This command does nothing if any of the specified keys already exist.

### Incorrect Pairing

Failing to provide key-value pairs correctly (e.g., an odd number of arguments) results in an error.

## FAQs

### How is `MSETNX` different from `MSET`?

`MSET` unconditionally sets all specified keys to their respective values, potentially overwriting existing keys. In contrast, `MSETNX` only sets the keys if none of them already exist.

### Can I use `MSETNX` with a single key-value pair?

Yes, but it behaves similarly to `SETNX` in such cases, setting the key only if it doesn't exist.
