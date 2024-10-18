---
description: Discover the use of Redis DECR for decrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECR

<PageTitle title="Redis DECR Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `DECR` command is used to decrement the integer value of a key by `1`.
This is especially useful when implementing counters, rate-limiters, or managing resources where you need to count down.

## Syntax

```shell
DECR key
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @string, @fast

## Parameter Explanations

- `key`: The name of the key whose value will be decremented by `1`. The key must hold a string that is an integer.

## Return Values

The command returns the value of the key after the decrement operation.

## Code Examples

### Basic Example

Decrement the value of a key:

```shell
dragonfly> SET mycounter 5
OK
dragonfly> DECR mycounter
(integer) 4
```

In this example, the value of `mycounter` is decremented from `5` to `4`.

### Decrement Non-Existent Key

If the key does not exist, `DECR` initializes the value to `0` before performing the decrement:

```shell
dragonfly> DECR not_yet_set
(integer) -1
```

Here, since `not_yet_set` did not previously exist, it is initialized to `0` and then decremented to `-1`.

### Using `DECR` for Countdown Timer

You can easily implement a countdown timer using `DECR`, which decrements until a limit is reached:

```shell
dragonfly> SET countdown 10
OK
dragonfly> DECR countdown
(integer) 9
dragonfly> DECR countdown
(integer) 8
dragonfly> DECR countdown
(integer) 7
dragonfly> DECR countdown
(integer) 6
```

Each `DECR` call reduces the value by `1`, simulating a countdown from `10` to `6`.

## Best Practices

- Ensure that the value stored under the key is a valid integer before calling `DECR`. If the value cannot be parsed as an integer, an error will be returned.
- You can use `DECR` in combination with `INCR` to create counters that can increase or decrease based on specific application logic.

## Common Mistakes

- Using `DECR` on a key that holds a non-integer, such as a string that cannot be parsed as a number. This will result in an error.

```shell
dragonfly> SET mykey "abc"
OK
dragonfly> DECR mykey
(error) ERR value is not an integer or out of range
```

- Forgetting that if the key does not exist, `DECR` will treat its value as `0` and then decrement it.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `DECR` behaves as if the key’s value is `0`, then decrements to `-1`.

### Is it possible to decrement a key while also checking if the value is a valid number?

No, `DECR` will fail if the key already holds a value that is not parsable as an integer. You need to ensure beforehand that the key contains a valid number or handle errors gracefully when calling `DECR`.

### Can I use `DECR` to decrement a very large number?

Yes, `DECR` can handle very large integers, but keep in mind there is a limit imposed by Redis's storage of integers. The maximum and minimum values typically correspond to the range of signed 64-bit integers.
