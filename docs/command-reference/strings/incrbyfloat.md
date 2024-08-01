---
description: Discover how to use Redis INCRBYFLOAT to increment a key's float value.
---

import PageTitle from '@site/src/components/PageTitle';

# INCRBYFLOAT

<PageTitle title="Redis INCRBYFLOAT Explained (Better Than Official Docs)" />

## Introduction

`INCRBYFLOAT` is a Redis command used to increment the value of a key by a specified floating-point number. It is essential for applications requiring precise numerical operations, such as financial calculations or real-time analytics.

## Syntax

```
INCRBYFLOAT key increment
```

## Parameter Explanations

- **key**: The name of the key whose value you want to increment. The key must contain a string that can be interpreted as a floating-point number.
- **increment**: The floating-point number by which the key’s value should be increased. This can be a positive or negative number.

## Return Values

The command returns the new value of the key after the increment operation, formatted as a string.

#### Example Outputs

```cli
dragonfly> SET mykey "10.50"
OK
dragonfly> INCRBYFLOAT mykey 0.1
"10.60"
dragonfly> INCRBYFLOAT mykey -5
"5.60"
```

## Code Examples

### Basic Example

Incrementing the value of a key by a floating-point number:

```cli
dragonfly> SET price "19.99"
OK
dragonfly> INCRBYFLOAT price 1.01
"21.00"
```

### Real-Time Analytics

Use `INCRBYFLOAT` for updating metrics in real-time:

```cli
# Increment page view count
dragonfly> SET page_views "100.5"
OK
dragonfly> INCRBYFLOAT page_views 2.3
"102.8"
```

### Financial Calculations

Adjust account balances with high precision:

```cli
# Initial balance
dragonfly> SET account_balance "1050.75"
OK
# Deposit amount
dragonfly> INCRBYFLOAT account_balance 250.25
"1301.00"
# Withdraw amount
dragonfly> INCRBYFLOAT account_balance -100.50
"1200.50"
```

## Best Practices

- Ensure the key's value is always a valid floating-point number before performing increment operations.
- Use `INCRBYFLOAT` over multiple commands (e.g., `GET`, compute, and `SET`) to avoid race conditions in concurrent environments.

## Common Mistakes

- Using `INCRBYFLOAT` on keys that do not contain numeric values will result in an error.
- Forgetting that the returned value is a string can lead to issues in strict type-checking environments.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `INCRBYFLOAT` initializes it to `0` before performing the increment.

### Can I decrement using `INCRBYFLOAT`?

Yes, by providing a negative increment value, you can effectively decrement the key’s value.

### What types of values can `INCRBYFLOAT` handle?

`INCRBYFLOAT` works with any string that can be parsed as a floating-point number, including scientific notation.
