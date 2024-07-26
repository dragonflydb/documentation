---
description: Discover the use of Redis DECR for decrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECR

<PageTitle title="Redis DECR Explained (Better Than Official Docs)" />

## Introduction

The `DECR` command in Redis is used to decrement the integer value of a key by one. If the key does not exist, it is set to 0 before performing the operation. This command is useful for counters and managing sequences.

## Syntax

```plaintext
DECR key
```

## Parameter Explanations

- **key**: The name of the key whose value you want to decrement. The key must hold an integer value.

## Return Values

The `DECR` command returns the value of the key after the decrement operation is performed.

### Example Output

- If the key exists:
  ```plaintext
  (integer) new_value
  ```
- If the key does not exist:
  ```plaintext
  (integer) -1
  ```

## Code Examples

### Basic Example

This example demonstrates how to use the `DECR` command to decrement a value:

```cli
dragonfly> SET mycounter 10
OK
dragonfly> DECR mycounter
(integer) 9
dragonfly> DECR mycounter
(integer) 8
dragonfly> GET mycounter
"8"
```

### Inventory Management

Decrementing stock quantity when an item is sold:

```cli
dragonfly> SET item:1001:stock 50
OK
dragonfly> DECR item:1001:stock
(integer) 49
dragonfly> GET item:1001:stock
"49"
```

### Rate Limiting

Reducing the allowed number of user actions per minute:

```cli
dragonfly> SET user:1234:rate_limit 5
OK
dragonfly> DECR user:1234:rate_limit
(integer) 4
dragonfly> GET user:1234:rate_limit
"4"
```

### Countdown Timer

Using `DECR` to implement a countdown timer:

```cli
dragonfly> SET countdown 10
OK
dragonfly> DECR countdown
(integer) 9
dragonfly> DECR countdown
(integer) 8
dragonfly> GET countdown
"8"
```

## Best Practices

- Ensure that the key holds an integer value; otherwise, the command will result in an error.
- Use the `DECR` command in atomic operations to avoid race conditions in concurrent environments.

## Common Mistakes

- Attempting to decrement a non-integer value will result in an error:
  ```cli
  dragonfly> SET mykey "hello"
  OK
  dragonfly> DECR mykey
  (error) ERR value is not an integer or out of range
  ```

## FAQs

### What happens if the key does not exist?

If the key does not exist, `DECR` sets it to 0 before performing the decrement operation. Hence, the first call to `DECR` will return -1.

### Can I use `DECR` on a key holding a negative integer?

Yes, `DECR` works with negative integers as well:

```cli
dragonfly> SET negcounter -10
OK
dragonfly> DECR negcounter
(integer) -11
dragonfly> GET negcounter
"-11"
```
