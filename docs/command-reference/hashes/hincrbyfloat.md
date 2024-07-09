---
description: "Learn how to use Redis HINCRBYFLOAT command to increment the float value of a hash field with precision."
---

import PageTitle from '@site/src/components/PageTitle';

# HINCRBYFLOAT

<PageTitle title="Redis HINCRBYFLOAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`HINCRBYFLOAT` is a Redis command used to increment the value of a specified field in a hash by a floating-point number. This command is particularly useful in scenarios where you need to track and update numeric values that require decimal precision, such as accounting balances, scientific measurements, or any other metrics stored in hashes.

## Syntax

```plaintext
HINCRBYFLOAT key field increment
```

## Parameter Explanations

- `key`: The name of the hash.
- `field`: The field within the hash whose value should be incremented.
- `increment`: The floating-point number by which to increment the field's value. This can be positive or negative.

## Return Values

The command returns the new value of the field after the increment operation, represented as a string.

### Example Outputs

- If the initial value is `1.5` and the increment is `0.5`, the return value would be `"2.0"`.
- If the initial value is `1.0` and the increment is `-1.1`, the return value would be `"-0.1"`.

## Code Examples

```cli
dragonfly> HSET myhash field1 "10.5"
(integer) 1
dragonfly> HINCRBYFLOAT myhash field1 0.5
"11.0"
dragonfly> HINCRBYFLOAT myhash field1 -2.3
"8.7"
dragonfly> HGET myhash field1
"8.7"
```

## Best Practices

When using `HINCRBYFLOAT`, ensure that the field contains a valid float representation. If the field does not exist, Redis initializes it to `0` before performing the increment.

## Common Mistakes

- **Non-numeric Fields**: Attempting to use `HINCRBYFLOAT` on a field that does not contain a numeric value will result in an error.
- **Data Type Misuse**: Using `HINCRBYFLOAT` on keys that are not hashes (e.g., strings, lists) will result in an error.

## FAQs

### What happens if the field does not exist?

If the field does not exist, `HINCRBYFLOAT` initializes the field to `0` and then performs the increment.

### Can the increment be a negative number?

Yes, the increment provided can be a negative floating-point number, effectively decrementing the field’s value.
