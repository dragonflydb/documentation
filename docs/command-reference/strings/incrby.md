---
description: Learn to use Redis INCRBY to increase the integer value of a key by a given amount.
---

import PageTitle from '@site/src/components/PageTitle';

# INCRBY

<PageTitle title="Redis INCRBY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `INCRBY` command in Redis is used to increment the integer value of a key by a specified amount. This command is commonly used for counters, such as page views, user sessions, or any metric that requires continuous incrementing.

## Syntax

```plaintext
INCRBY key increment
```

## Parameter Explanations

- **key**: The name of the key whose value you want to increment. It must contain a string integer.
- **increment**: The amount by which to increment the key's value. This must be an integer and can be positive or negative.

## Return Values

The `INCRBY` command returns the new value of the key after the increment operation.

Example:

```cli
dragonfly> INCRBY mycounter 10
(integer) 20
```

## Code Examples

```cli
dragonfly> SET mycounter 100
OK
dragonfly> INCRBY mycounter 5
(integer) 105
dragonfly> INCRBY mycounter -3
(integer) 102
dragonfly> GET mycounter
"102"
```

## Best Practices

- Ensure the initial value of the key is set before using `INCRBY`, as operating on a non-existent key will initialize it with a value of 0.
- Use atomic operations like `INCRBY` in multi-step commands to avoid race conditions.

## Common Mistakes

- Using `INCRBY` on keys that do not store integer values will result in an error.
- Forgetting that `INCRBY` can only work on integers; attempting to use it with non-integer strings will cause failures.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `INCRBY` will create the key and set its initial value to the increment amount.

### Can I use `INCRBY` with floating-point numbers?

No, `INCRBY` only works with integer values. For floating-point increments, use the `INCRBYFLOAT` command instead.

### What if the key contains a non-numeric value?

If the key contains a value that cannot be interpreted as an integer, Redis will return an error.
