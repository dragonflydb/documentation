---
description: Learn how Redis GETSET sets a new value for a key & returns the old value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETSET

<PageTitle title="Redis GETSET Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GETSET` command is used to atomically set a key to a new string value and return its old string value.
This command is useful when you need to replace a value but also want to keep track of the previous value before overwriting it, making it an atomic and efficient way to perform this operation.

## Syntax

```shell
GETSET key value
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key whose value should be replaced.
- `value`: The new value to set the key to.

## Return Values

The command returns the old value that was stored at the key before it was set to the new value.
If the key did not exist, it returns `nil`.

## Code Examples

### Basic Example

Set a key to a new value and retrieve the old value:

```shell
dragonfly$> SET mykey "old_value"
OK
dragonfly$> GETSET mykey "new_value"
"old_value"
```

If the key does not exist yet, `GETSET` will return `nil`:

```shell
dragonfly$> GETSET mykey2 "first_value"
(nil)
```

### Using `GETSET` for Atomic Value Updates

This command is particularly useful when you want to update a key's value atomically while preserving the old value for further use or inspection:

```shell
# User balance system where balance is first saved, then updated atomically
dragonfly$> SET balance "100"
OK
dragonfly$> GETSET balance "200"
"100"  # Old balance
dragonfly$> GET balance
"200"  # New balance
```

### `GETSET` in Cache Systems

In cache systems, `GETSET` is great for refreshing stale values atomically:

```shell
# Set initial cache value
dragonfly$> SET cache_item "stale_value"
OK

# Atomically refresh the cache with a new value, returning the old one
dragonfly$> GETSET cache_item "fresh_value"
"stale_value"

# Verify that the value has been updated
dragonfly$> GET cache_item
"fresh_value"
```

## Best Practices

- Use `GETSET` when you need atomicity in replacing a value and retrieving the previous one.
- Be cautious when using `GETSET` in high-write workloads, as it can be slower than using `SET` on its own, due to the need to return the old value.

## Common Mistakes

- Trying to use `GETSET` on non-string values like lists, sets, or hashes; it only works on string values.
- Assuming that it will return something other than `nil` for non-existent keys.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETSET` will return `nil` and set the key to the new value.

### Can `GETSET` be used with non-string values such as lists or sets?

No, `GETSET` only works with string values.
For non-string data types, consider using other commands like `LINDEX` for lists or `HGETSET` for hashes.

### Is `GETSET` atomic?

Yes, `GETSET` is atomic, meaning it safely sets the new value and retrieves the old value in one single operation.
This helps avoid race conditions in concurrent environments.
