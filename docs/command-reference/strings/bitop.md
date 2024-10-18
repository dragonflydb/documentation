---
description: Learn how to conduct bitwise operations on strings using Redis BITOP.
---

import PageTitle from '@site/src/components/PageTitle';

# BITOP

<PageTitle title="Redis BITOP Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BITOP` command is used to perform bitwise operations between multiple keys and store the result in a destination key.
It supports operations like `AND`, `OR`, `XOR`, and `NOT`.
This command is crucial for handling binary data and performing efficient bulk bitwise operations.

## Syntax

```shell
BITOP operation destkey key [key ...]
```

- **Time complexity:** O(N) where N is the size of the string inputs.
- **ACL categories:** @write, @bitmap, @slow

## Parameter Explanations

- `operation`: The bitwise operation to be performed. It can be `AND`, `OR`, `XOR`, or `NOT`.
- `destkey`: The key where the result of the bitwise operation will be stored.
- `key [key ...]`: One or more keys containing string values on which the bitwise operation will be applied.

## Return Values

Returns the size of the string stored in the destination key, measured in bytes.

## Code Examples

### Basic Example

Performing a basic bitwise `AND` operation between two keys:

```shell
dragonfly> SET key1 "foobar"
OK
dragonfly> SET key2 "abcdef"
OK
dragonfly> BITOP AND result key1 key2
(integer) 6
dragonfly> GET result
"\x60\x60\x04\x00\x00\x00"
```

### Combining Multiple Keys with the `OR` Operation

Combining three keys using the `OR` operation:

```shell
dragonfly> SET key1 "\x01"
OK
dragonfly> SET key2 "\x02"
OK
dragonfly> SET key3 "\x03"
OK
dragonfly> BITOP OR result key1 key2 key3
(integer) 1
dragonfly> GET result
"\x03"
```

### Using the `XOR` Operation

Using the `XOR` operation to combine two keys:

```shell
dragonfly> SET key1 "\x0F"
OK
dragonfly> SET key2 "\xF0"
OK
dragonfly> BITOP XOR result key1 key2
(integer) 1
dragonfly> GET result
"\xFF"
```

### Using the `NOT` Operation

Performing the `NOT` operation on a single key:

```shell
dragonfly> SET key1 "\xAA"  # 10101010 in binary
OK
dragonfly> BITOP NOT result key1
(integer) 1
dragonfly> GET result
"\x55"  # 01010101 in binary (inverted bits)
```

## Best Practices

- Ensure the keys involved in the `BITOP` operation have values of the same length for predictable results.
- Use the `NOT` operation with only one key, as this is the only unary operation in `BITOP`.

## Common Mistakes

- Using the `NOT` operation with more than one key will result in an error.
- Performing operations on non-string data types can lead to unexpected results or errors.

## FAQs

### What happens if the keys have different lengths?

Redis pads the shorter strings with zero bytes to match the length of the longest string before performing the bitwise operation.

### Can I use `BITOP` with empty keys?

Yes, but if all keys are empty, the result stored in the destination key will also be an empty string.
