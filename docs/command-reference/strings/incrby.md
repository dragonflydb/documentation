---
description: Learn to use Redis INCRBY to increase the integer value of a key by a given amount.
---

import PageTitle from '@site/src/components/PageTitle';

# INCRBY

<PageTitle title="Redis INCRBY Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `INCRBY` command allows you to increment the value of a key by a specified integer amount.
This is particularly useful when working with counters or any numerical values that need to be incremented atomically.
If the key does not exist, `INCRBY` will create the key with an initial value of `0` before performing the increment operation.

## Syntax

```shell
INCRBY key increment
```

## Parameter Explanations

- `key`: The name of the key whose value you want to increment.
- `increment`: The integer amount by which to increment the current value at the key.

## Return Values

The command returns the new value of the key, which is the result of adding the specified increment to the current value.

## Code Examples

### Basic Example

Increment a key by `5`:

```shell
dragonfly> SET mycounter 10
OK
dragonfly> INCRBY mycounter 5
(integer) 15
```

In this example, the value of `mycounter` is initially `10`, and after executing `INCRBY mycounter 5`, the new value becomes `15`.

### Increment a Non-Existent Key

If the key does not exist, `INCRBY` will first set it to `0` and then increment it by the specified value:

```shell

dragonfly> INCRBY newcounter 4
(integer) 4
```

Here, `newcounter` did not exist initially.
`INCRBY` creates the key and sets its value to `4` as there was no existing value to increment.

### Using Negative Increments

You can also decrement a key by passing a negative number as the increment value:

```shell
dragonfly> SET score 20
OK
dragonfly> INCRBY score -7
(integer) 13
```

In this example, `INCRBY` is used with a negative value of `-7` to decrement the key `score` from `20` to `13`.

### Multiple Increments

Increment the same key multiple times with different values:

```shell
dragonfly> SET visits 100
OK
dragonfly> INCRBY visits 10
(integer) 110
dragonfly> INCRBY visits 15
(integer) 125
```

Here, the value of `visits` is incremented twice, first by `10` and then by `15`, resulting in a final value of `125`.

## Best Practices

- Use `INCRBY` for maintaining counters or other numeric accumulations that need to be updated atomically.
- Keep in mind that if you are dealing with non-integer values, this command does not support floating-point numbers.
  For floats, use `INCRBYFLOAT` instead.

## Common Mistakes

- Applying `INCRBY` to a key that holds a non-integer value will result in an error.
  Ensure that the key either contains an integer or does not exist when using this command.
- Using `INCRBY` with a key that stores a non-numeric value will cause an error and fail:

  ```shell
  dragonfly> SET mystring "hello"
  OK
  dragonfly> INCRBY mystring 2
  (error) ERR value is not an integer or out of range
  ```

- Trying to increment large numerical values that exceed the 64-bit signed integer limit may result in an overflow error.

## FAQs

### What happens if the key holds a string value instead of an integer?

If the key holds a string, list, or another non-integer value, `INCRBY` will return an error.
The key must either be unset or holding an integer value to execute successfully.

### Can I use `INCRBY` with floating-point numbers?

No, `INCRBY` only works with integers.
If you need to increment by a floating-point number, you should use the `INCRBYFLOAT` command.

### What’s the maximum increment value I can use?

`INCRBY` supports 64-bit signed integers.
As such, the maximum allowable increment would be `9,223,372,036,854,775,807`, and the minimum would be `-9,223,372,036,854,775,808`.
