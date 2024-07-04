---
description: Learn how to use Redis DECRBY to decrease the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECRBY

<PageTitle title="Redis DECRBY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `DECRBY` command in Redis is used to decrement the integer value of a key by a given number. This is useful in scenarios where you need to efficiently decrease counters, such as tracking the number of remaining items in inventory, countdown timers, or similar use cases where a numerical reduction is required.

## Syntax

```
DECRBY key decrement
```

## Parameter Explanations

- **key**: The name of the key whose value you want to decrement. The value stored at the key must be a string representing an integer.
- **decrement**: The integer value by which the key's value will be decreased.

## Return Values

The command returns the value of the key after the decrement operation.

Example:

```cli
dragonfly> SET mycounter 10
OK
dragonfly> DECRBY mycounter 3
(integer) 7
```

## Code Examples

```cli
dragonfly> SET mycounter 5
OK
dragonfly> DECRBY mycounter 2
(integer) 3
dragonfly> DECRBY mycounter 4
(integer) -1
```

## Best Practices

- Ensure that the key holds an integer value before using `DECRBY`. If the key does not exist, Redis initializes it to 0 before performing the operation.
- Be aware of potential underflows if decrements drive the value below the minimum integer representable in Redis.

## Common Mistakes

- Using `DECRBY` on a key containing non-integer values will result in an error.
- Forgetting that if the key does not exist, Redis will treat it as if it was set to 0.

## FAQs

### What happens if the key does not exist?

If the key does not exist, Redis initializes it to 0 and then performs the decrement.

### Can I use `DECRBY` with a float value?

No, `DECRBY` only works with integer values. For floating-point operations, consider using `INCRBYFLOAT`.

### What is the maximum decrement I can apply?

You can apply any decrement within the range of valid integer values in Redis, which is typically bounded by the limits of signed 64-bit integers.
