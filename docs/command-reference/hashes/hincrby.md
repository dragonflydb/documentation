---
description: "Learn how to use Redis HINCRBY command to increment the integer value of a hash field."
---

import PageTitle from '@site/src/components/PageTitle';

# HINCRBY

<PageTitle title="Redis HINCRBY Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `HINCRBY` command in Redis is used to increment the integer value of a field in a hash by a specified amount. This command is useful in scenarios where you need to perform atomic increments on counters stored within hashes, such as tracking user scores, inventory counts, or any other numeric data that requires incremental updates.

## Syntax

```
HINCRBY key field increment
```

## Parameter Explanations

- **key**: The name of the hash.
- **field**: The field within the hash whose value you want to increment.
- **increment**: The amount by which to increment the field's value. This can be a positive or negative integer.

## Return Values

The `HINCRBY` command returns the value of the field after the increment operation is applied.

### Example Outputs

- If the field does not exist before the operation:
  ```cli
  (integer) 10
  ```
- If the field exists and its value is incremented:
  ```cli
  (integer) 20
  ```

## Code Examples

```cli
dragonfly> HSET myhash field1 5
(integer) 1
dragonfly> HINCRBY myhash field1 10
(integer) 15
dragonfly> HINCRBY myhash field2 -5
(integer) -5
dragonfly> HGETALL myhash
1) "field1"
2) "15"
3) "field2"
4) "-5"
```

## Best Practices

- Ensure that the fields you intend to increment are initialized appropriately.
- Use `HINCRBY` for atomic operations to avoid race conditions in concurrent environments.

## Common Mistakes

- Using non-integer values for increments can lead to errors. Always ensure the increment value is an integer.
- Attempting to increment a field containing non-numeric data will result in an error.

## FAQs

### What happens if the field does not exist before invoking `HINCRBY`?

If the field does not exist, `HINCRBY` initializes it to 0 before applying the increment.

### Can I use `HINCRBY` with floating-point numbers?

No, `HINCRBY` only supports integer increments. For floating-point number increments, use the `HINCRBYFLOAT` command.
