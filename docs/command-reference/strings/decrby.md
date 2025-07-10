---
description: Learn how to use Redis DECRBY to decrease the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECRBY

<PageTitle title="Redis DECRBY Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `DECRBY` command is used to decrement the integer value of a key by a specified amount.
This command is particularly useful for counters, resource quotas, or rate-limiting scenarios where you want to decrease a value atomically with minimal overhead.

## Syntax

```shell
DECRBY key decrement
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key associated with the integer value that will be decremented.
- `decrement`: The decrement amount, which is a signed integer. The value will be subtracted from the current value of the key.

## Return Values

The command returns the integer result after the decrement operation is performed on the value of the key.

## Code Examples

### Basic Example

Decrement the value stored at a key by a specified amount:

```shell
dragonfly$> SET mycounter 10
OK
dragonfly$> DECRBY mycounter 3
(integer) 7
```

### Using Non-Existent Keys

If the key does not exist, `DECRBY` assumes the initial value to be `0`:

```shell
dragonfly$> DECRBY non_existent 5
(integer) -5
```

### Decrementing by a Negative Value (Effectively Incrementing)

You can provide a negative `decrement` to increase the value:

```shell
dragonfly$> SET score 50
OK
dragonfly$> DECRBY score -10
(integer) 60  # Effectively increments by 10
```

### Handling Large Decrement Values

You can use large decrement values, but the key's value must always remain within the 64-bit signed integer limit:

```shell
dragonfly$> SET largekey 1000000000000
OK
dragonfly$> DECRBY largekey 999999999999
(integer) 1
```

## Best Practices

- Ensure the value of the key is always an integer or can be interpreted as an integer, otherwise a failure will occur.
- Avoid using excessive large decrements that push the value beyond the bounds of a signed 64-bit integer, since this will generate an overflow error.
- For scenarios such as rate-limiting or quotas, always check the resulting value after decrementing to ensure it has not gone below the allowed threshold.

## Common Mistakes

- Using `DECRBY` on keys that don't contain numeric values, such as strings, will result in an error.
- Assuming that the command creates a new `key` with the specified value, when the behavior for non-existent keys is to start with `0` instead.

## FAQs

### What happens if the key is not an integer or the value is non-numeric?

The `DECRBY` command will return an error if the key holds a value that is not an integer or cannot be interpreted as such.

### Can I decrement the value of a key by `0`?

Yes, decrementing by `0` will simply return the current value of the key without making any changes.

### What happens if I try to decrement a value outside the range of a 64-bit signed integer?

If you attempt to decrement a value beyond the supported range for 64-bit signed integers, you'll receive an overflow error.
