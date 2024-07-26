---
description: Learn how to use Redis INCR command for incrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# INCR

<PageTitle title="Redis INCR Explained (Better Than Official Docs)" />

## Introduction

The `INCR` command in Redis is used to increment the integer value of a key by one. If the key does not exist, it is created with the value 0 before performing the increment operation. This command is essential for counters, rate limiting, and managing sequences in Redis.

## Syntax

```plaintext
INCR key
```

## Parameter Explanations

- `key`: The key whose value you want to increment. It must hold an integer value or be non-existent (in which case it will be initialized to 0).

## Return Values

`INCR` returns the new value of the key after the increment operation.

#### Example Outputs

- If `mykey` holds the value 10 before the increment: `(integer) 11`
- If `mykey` does not exist before the increment: `(integer) 1`

## Code Examples

### Basic Example

Incrementing a non-existent key:

```cli
dragonfly> INCR mycounter
(integer) 1
```

Incrementing an existing key:

```cli
dragonfly> SET mycounter 5
OK
dragonfly> INCR mycounter
(integer) 6
```

### Page View Counter

Using `INCR` to track page views:

```cli
dragonfly> INCR page:view:homepage
(integer) 1
dragonfly> INCR page:view:homepage
(integer) 2
```

### Rate Limiting

Implement a simple rate limiter that increments a counter every time an action is performed:

```cli
dragonfly> INCR user:1234:action_count
(integer) 1
```

### Generating Unique IDs

Create unique user IDs using `INCR`:

```cli
dragonfly> INCR user:id
(integer) 1
dragonfly> INCR user:id
(integer) 2
```

## Best Practices

- Ensure keys used with `INCR` are either non-existent or store integer values to avoid errors.
- Combine `INCR` with expiration commands like `EXPIRE` to auto-reset counters where necessary.

## Common Mistakes

- Using `INCR` on non-integer keys will result in an error:

  ```cli
  dragonfly> SET mystring "hello"
  OK
  dragonfly> INCR mystring
  (error) ERR value is not an integer or out of range
  ```

### What happens if the key already contains a non-integer value?

Attempting to increment a key holding a non-integer value will result in an error.

### Can I use `INCR` with floating-point numbers?

No, `INCR` only works with integers. Use `INCRBYFLOAT` for floating-point increments.
