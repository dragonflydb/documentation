---
description: Understand how Redis GETBIT retrieves a specific bit from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETBIT

<PageTitle title="Redis GETBIT Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GETBIT` command is used to retrieve the bit value (either `0` or `1`) at a specific position in a string.
The command allows you to efficiently access individual bits stored in a string, making it particularly useful for scenarios such as bitwise operations, feature flags, or binary statuses.

## Syntax

```shell
GETBIT key offset
```

- **Time complexity:** O(1)
- **ACL categories:** @read, @bitmap, @fast

## Parameter Explanations

- `key`: The key of the string holding the value where the bit is extracted.
- `offset`: The bit offset (zero-based index) to retrieve from. The first bit of the string is at offset `0`.

## Return Values

The command will return either `0` or `1`, corresponding to the bit value at the specified `offset`.
If the `offset` exceeds the length of the string (in bits), the command returns `0`.

## Code Examples

### Basic Example

Retrieve a bit at a specific position in a string:

```shell
# String: example
# Hex:    0x65     0x78     0x61     0x6d     0x70     0x6c     0x65
# Binary: 01100101 01111000 01100001 01101101 01110000 01101100 01100101
dragonfly> SET mykey "example"
OK
dragonfly> GETBIT mykey 1
(integer) 1  # The bit at position 1 is 1.
dragonfly> GETBIT mykey 6
(integer) 0  # The bit at position 6 is 0.
```

### Retrieving Bits Beyond the String Boundaries

Attempting to retrieve a bit beyond the length of the string:

```shell
# The length of the string "example" in bits is 56 (7 characters * 8 bits).
dragonfly> GETBIT mykey 100
(integer) 0  # Returns 0 because the offset is out of bounds.
```

### Using `GETBIT` in Binary Flags

In many use cases, each bit can signify a flag that is either enabled (`1`) or disabled (`0`):

```shell
dragonfly> SET flags "\x0F"  # Binary: 00001111 (four flags enabled)
OK
dragonfly> GETBIT flags 0
(integer) 0  # The first feature is disabled.
dragonfly> GETBIT flags 4
(integer) 1  # The fifth feature is enabled.
```

## Best Practices

- Consider compressing binary representations of data into strings and using `GETBIT` to check for specific flags or states.
- If you manage performance-sensitive applications, long strings should be accessed cautiously to avoid performance bottlenecks due to large bit offset calculations.

## Common Mistakes

- Using byte-level offsets when specifying the `offset` for `GETBIT`. The `offset` parameter works at the bit level, not at the byte level.
- Assuming that `GETBIT` modifies the string. This command only reads the specified bit without altering the string.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETBIT` returns `0` by default, as there is no bit set at any offset.

### Can I use negative offsets?

No, the `GETBIT` command does not support negative offsets. You must provide a non-negative integer.
