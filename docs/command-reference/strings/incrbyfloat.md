---
description: Discover how to use Redis INCRBYFLOAT to increment a key's float value.
---

import PageTitle from '@site/src/components/PageTitle';

# INCRBYFLOAT

<PageTitle title="Redis INCRBYFLOAT Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `INCRBYFLOAT` command is used to increment the value of a key by a specified floating-point number.
This command is particularly useful when you need to store numerical data and perform frequent updates with floating-point precision, such as tracking scores, balances, or statistics.

If the key does not exist, `INCRBYFLOAT` will initialize it to `0` before executing the operation.

## Syntax

```shell
INCRBYFLOAT key increment
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key where the number is stored.
- `increment`: The floating-point number by which to increment the value.

## Return Values

The command returns the new floating-point value after the increment.

## Code Examples

### Basic Example

Increment the float value of a key:

```shell
dragonfly$> SET counter 10.5
OK
dragonfly$> INCRBYFLOAT counter 1.5
"12"
```

Here, the value stored at `counter` is updated from `10.5` to `12` after adding `1.5`.

### Initializing and Incrementing Non-Existent Keys

If the key does not exist, it is initialized to `0` before incrementing by the specified amount.

```shell

dragonfly$> INCRBYFLOAT new_counter 2.5
"2.5"
```

### Negative Floating-Point Increments

You can also use negative numbers to decrement the value:

```shell
dragonfly$> SET score 20.0
OK
dragonfly$> INCRBYFLOAT score -5.5
"14.5"
```

### Handling High Precision Increments

`INCRBYFLOAT` maintains float precision, allowing fine-grained changes, such as adding a small decimal value:

```shell
dragonfly$> SET balance 150.0
OK
dragonfly$> INCRBYFLOAT balance 0.03
"150.03"
```

### Multiple Increments on the Same Key

You can repeatedly increment the same key for cumulative updates:

```shell
dragonfly$> SET total 100.0
OK
dragonfly$> INCRBYFLOAT total 10.7
"110.7"
dragonfly$> INCRBYFLOAT total 2.3
"113"
```

## Best Practices

- Use `INCRBYFLOAT` when you need arithmetic operations that require floating-point precision.
- Be cautious when performing many small floating-point increments, as precision drift might occur over time.
- Consider using this command for tracking metrics or scores where floating-point precision is essential.

## Common Mistakes

- Incrementing non-numeric values can throw an error, so always ensure the stored value is a valid number (or numeric string).
- Be aware that rounding errors are inherent to floating-point arithmetic, so the result might not have perfect precision for certain values.

## FAQs

### What happens if the key stores a non-numeric value?

If the key holds a non-numeric value, `INCRBYFLOAT` returns an error indicating that the value cannot be incremented.

### Can I decrement a number using `INCRBYFLOAT`?

Yes, providing a negative increment will effectively decrement the current value.

### Does `INCRBYFLOAT` work with integers?

While `INCRBYFLOAT` is designed for floating-point numbers, it can increment integer values as well. However, the result will always be returned as a floating-point number.
