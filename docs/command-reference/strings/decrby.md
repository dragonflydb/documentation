---
description: Learn how to use Redis DECRBY to decrease the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECRBY

<PageTitle title="Redis DECRBY Explained (Better Than Official Docs)" />

## Introduction

The `DECRBY` command in Redis decrements the integer value of a key by a specified amount. This command is useful for counters and can help manage quantities that decrease over time, such as inventory counts or countdown timers.

## Syntax

```plaintext
DECRBY key decrement
```

## Parameter Explanations

- **key**: The name of the key whose value you want to decrement. It should hold an integer value.
- **decrement**: The integer value by which the key's value will be decremented.

## Return Values

The `DECRBY` command returns the new value of the key after the decrement operation.

#### Example Output

If `mycounter` holds the value `10` and you run `DECRBY mycounter 3`, the return value will be `7`.

## Code Examples

### Basic Example

In this example, we decrement the value of a counter.

```cli
dragonfly> SET mycounter 10
OK
dragonfly> DECRBY mycounter 3
(integer) 7
dragonfly> DECRBY mycounter 2
(integer) 5
```

### Inventory Management

This example demonstrates using `DECRBY` to manage inventory levels.

```cli
dragonfly> SET product:1001:stock 20
OK
dragonfly> DECRBY product:1001:stock 5
(integer) 15
dragonfly> DECRBY product:1001:stock 3
(integer) 12
```

### Countdown Timer

This example shows how to implement a countdown timer using `DECRBY`.

```cli
dragonfly> SET countdown_timer 100
OK
dragonfly> DECRBY countdown_timer 10
(integer) 90
dragonfly> DECRBY countdown_timer 30
(integer) 60
```

## Best Practices

- Ensure the key holds an integer value before using `DECRBY` to avoid errors.
- Handle potential negative values if the decrement amount exceeds the current value.

## Common Mistakes

- Using `DECRBY` on a key that does not hold an integer value will result in an error.
- Forgetting that `DECRBY` can yield negative values, which may not be desirable for certain use cases like inventory management.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `DECRBY` treats it as if it holds the value `0` and sets the new value to `-decrement`.

### Can `DECRBY` handle floating-point numbers?

No, `DECRBY` only works with integer values. For decrementing floating-point numbers, consider other data structures or commands.
