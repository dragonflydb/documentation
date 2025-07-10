---
description: Learn how to use Redis INCR command for incrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# INCR

<PageTitle title="Redis INCR Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `INCR` command is used to atomically increment the integer value of a key by one.
This is helpful for implementing counters, tracking requests, or managing sequence numbers since it is thread-safe and operates in constant time `O(1)`.

## Syntax

```shell
INCR key
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The key whose value will be incremented by one. If the key doesn't exist, it will be automatically created with a value of `0` before being incremented.

## Return Values

Returns the new value of the key after the increment as an integer.

## Code Examples

### Basic Example

Increment an integer stored in a key:

```shell
dragonfly$> SET mykey 10
OK
dragonfly$> INCR mykey
(integer) 11
```

### Automatically Creating and Incrementing a Key

If the key does not exist, `INCR` will set it to `0` before incrementing it:

```shell
dragonfly$> EXISTS counter
(integer) 0
dragonfly$> INCR counter
(integer) 1
```

### Using `INCR` with Negative Numbers

`INCR` can handle negative numbers too.
It will still increase the value by one in this case:

```shell
dragonfly$> SET mykey -5
OK
dragonfly$> INCR mykey
(integer) -4
```

### Incrementing in a Loop

You can repeatedly call `INCR` to track a counter of operations:

```shell
dragonfly$> SET request_count 100
OK
dragonfly$> INCR request_count
(integer) 101
dragonfly$> INCR request_count
(integer) 102
```

## Best Practices

- Use `INCR` to implement performance-efficient counters due to its atomic nature.
- Consider using the `EXPIRE` command alongside to set TTLs for temporary counters, such as tracking hits in a web application.
- If you need to increment a value by something other than `1`, use the closely related `INCRBY` command, which allows you to specify the increment amount.

## Common Mistakes

- Trying to use `INCR` on non-integer or non-string values (e.g., lists or sets).
  This will result in an error, as `INCR` expects the value stored at `key` to be a string representation of an integer.

  ```shell
  dragonfly$> LPUSH mylist 1
  (integer) 1
  dragonfly$> INCR mylist
  (error) WRONGTYPE Operation against a key holding the wrong kind of value
  ```

- Not realizing that `INCR` only creates keys as integer strings when they don't exist.
  If you want to manipulate more complex data types, use other commands like `INCRBYFLOAT` for floats.

## FAQs

### What happens if the key contains a non-integer value?

You will get an error.
`INCR` expects the value at `key` to be a valid integer or an integer-convertible string (e.g., "10").

### Will `INCR` work with floating-point numbers?

No, `INCR` is meant for integer manipulation only.
For floating-point values, use the `INCRBYFLOAT` command, which is designed specifically for that purpose.

### What happens if the key does not exist?

If the key does not exist, `INCR` creates the key with a value of `0`, and then increments it by `1`.
So the first call to `INCR` will result in the value `1`.
