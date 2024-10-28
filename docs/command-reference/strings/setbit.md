---
description: Learn about Redis SETBIT to manipulate specific binary bits of a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# SETBIT

<PageTitle title="Redis SETBIT Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `SETBIT` command is used to set or clear the bit at a specific offset in the string value of a key.
It is a powerful command for performing bit-level operations in use cases such as storing feature flags, binary state tracking, or custom bit fields.

## Syntax

```shell
SETBIT key offset value
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @bitmap, @slow

## Parameter Explanations

- `key`: The key of the string where the bit will be set or cleared.
- `offset`: The position of the bit to modify, where `0` is the first bit. This is based on the **bit index**, not byte index.
- `value`: The value to set the bit to. This can be either `0` (clear the bit) or `1` (set the bit).

## Return Values

The command returns the original bit value that was at the specified `offset` before it was modified.

## Code Examples

### Basic Example: Setting and Getting a Bit

Set a bit at a specific offset and retrieve its original state:

```shell
dragonfly> SET mykey "foo"
OK
dragonfly> SETBIT mykey 7 1
(integer) 0  # The bit at offset 7 was originally 0, now set to 1.
dragonfly> GETBIT mykey 7
(integer) 1  # We just set this bit to 1.
```

### Setting and Clearing Bits

Example of switching bits on and off at different positions:

```shell
# Initial value: 01000001
dragonfly> SET mykey "A"
OK
dragonfly> SETBIT mykey 1 0
(integer) 1  # The bit at position 1 was originally 1.
dragonfly> SETBIT mykey 1 1
(integer) 0  # The bit was previously cleared, now set to 1.
dragonfly> GET mykey
"A"
```

### Using `SETBIT` for Feature Flags

Suppose you have a system where each bit in a string represents whether a feature is enabled or disabled for a user:

```shell
# Initial value: 00000000 (all features disabled)
dragonfly> SET mykey "\x00"
OK
dragonfly> SETBIT mykey 0 1  # Enable feature at position 0
(integer) 0
dragonfly> SETBIT mykey 4 1  # Enable feature at position 4
(integer) 0
dragonfly> GETBIT mykey 0
(integer) 1
dragonfly> GETBIT mykey 4
(integer) 1
dragonfly> getbit mykey 5
(integer) 0
dragonfly> GET mykey
"\x88"  # Binary: 10001000
```

## Best Practices

- Use `SETBIT` and other bitmap-related commands when you need to store and manipulate binary data efficiently without the overhead of larger data structures like lists.
- When working with large binary datasets, combine `GETBIT` and `BITCOUNT` to efficiently track the state of multiple items.

## Common Mistakes

- Confusing the `offset` as a byte index instead of a bit index.
- Setting a bit at an offset that is beyond the length of the string can automatically expand the string, filling the unspecified bits in between with `0`.

## FAQs

### What happens if the key does not exist?

If the key does not exist, a new string is created with enough bytes to accommodate the specified `offset`. All bits in the new string are initialized to `0` except for the bit that is explicitly set.

### Can I specify an `offset` beyond the current string length?

Yes, specifying an `offset` beyond the current string length results in the expansion of the string. The new bits between the old string length and the new `offset` are filled with `0`.

### What happens if the `value` is neither `0` nor `1`?

Attempting to set a bit with a `value` other than `0` or `1` returns an error.
