---
description: Learn how to use Redis INCR command for incrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# INCR

<PageTitle title="Redis INCR Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `INCR` command in Redis is used to increment the integer value of a key by one. If the key does not exist, it is set to 0 before performing the operation. This command is useful in scenarios where you need to keep track of counts, such as page hits, number of user logins, or any other sequentially increasing metric.

## Syntax

```
INCR key
```

## Parameter Explanations

- **key**: The key whose value you want to increment. This should be a string representing an integer. If the key does not exist, it will be created with a value of 0 before being incremented.

## Return Values

The `INCR` command returns the value of the key after the increment.

Example outputs:

- If the initial value of `mycounter` is 10:
  ```cli
  dragonfly> INCR mycounter
  (integer) 11
  ```
- If the key `mycounter` does not exist:
  ```cli
  dragonfly> INCR mycounter
  (integer) 1
  ```

## Code Examples

```cli
dragonfly> SET mycounter 10
OK
dragonfly> INCR mycounter
(integer) 11
dragonfly> INCR mycounter
(integer) 12
dragonfly> DEL mycounter
(integer) 1
dragonfly> INCR mycounter
(integer) 1
```

## Best Practices

- Ensure that the key's value is always an integer. Using `INCR` on a key containing non-integer values will result in an error.
- Use `INCR` for thread-safe atomic increments. This avoids race conditions in distributed environments.

## Common Mistakes

- **Using `INCR` on non-integer keys**: If you try to increment a key that holds a string or another data type, an error will occur.
  ```cli
  dragonfly> SET mykey "hello"
  OK
  dragonfly> INCR mykey
  (error) ERR value is not an integer or out of range
  ```

## FAQs

### What happens if I use `INCR` on a non-existent key?

If the key does not exist, Redis treats it as if it were set to 0 and then performs the increment operation, resulting in a value of 1.

### Can I decrement a key using the `INCR` command?

No, to decrement a key, you would use the `DECR` command.
