---
description: Discover how to use Redis INCRBYFLOAT to increment a key's float value.
---

import PageTitle from '@site/src/components/PageTitle';

# INCRBYFLOAT

<PageTitle title="Redis INCRBYFLOAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `INCRBYFLOAT` command in Redis increments the numeric value of a key by a specified floating-point number. It's particularly useful for counters, real-time analytics, or any application where you need to perform precise incremental calculations.

## Syntax

```cli
INCRBYFLOAT key increment
```

## Parameter Explanations

- **key**: The name of the key whose value you want to increment.
- **increment**: The floating-point number by which to increase the key's value. This can be a positive or negative number.

## Return Values

The command returns the new value of the key after the increment. If the key does not exist, it is set to 0 before performing the operation.

Example outputs:

- If the initial value is 10.5 and you run `INCRBYFLOAT key 2.3`, the output will be `12.8`.
- If the key does not exist and you run `INCRBYFLOAT key 1.1`, the output will be `1.1`.

## Code Examples

```cli
dragonfly> SET mykey 10.50
OK
dragonfly> INCRBYFLOAT mykey 0.10
"10.60"
dragonfly> INCRBYFLOAT mykey -5.25
"5.35"
dragonfly> GET mykey
"5.35"
dragonfly> INCRBYFLOAT newkey 1.23
"1.23"
dragonfly> GET newkey
"1.23"
```

## Best Practices

- Ensure that the key contains a value that can be interpreted as a floating-point number to avoid errors.
- Use this command for precise increment operations, especially in applications requiring high accuracy like financial calculations or scientific data processing.

## Common Mistakes

- Using `INCRBYFLOAT` on a key that does not store a string representation of a float will result in an error. For example, trying to use `INCRBYFLOAT` on a key holding non-numeric data will fail.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `INCRBYFLOAT` sets it to 0 before applying the increment.

### Can I decrement the value using `INCRBYFLOAT`?

Yes, you can decrement the value by specifying a negative increment.

### What type of data does the key need to hold for `INCRBYFLOAT` to work?

The key should hold a string that represents a floating-point number. Any other type will result in an error.
