---
description: Discover how to find the position of a bit set to 1 or 0 in a string with Redis BITPOS.
---

import PageTitle from '@site/src/components/PageTitle';

# BITPOS

<PageTitle title="Redis BITPOS Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BITPOS` command is used to find the first occurrence of a bit set to `1` or `0` in a binary string.
This command is particularly useful for efficiently locating bit transitions and is commonly used in scenarios like sparse data structures, flags, or low-level data processing.

## Syntax

```shell
BITPOS key bit [start [end [BYTE|BIT]]]
```

## Parameter Explanations

- `key`: The key of the string in which the search will occur.
- `bit`: The bit value to search for, which can be either `0` or `1`.
- `start` (optional): The starting byte position from which to begin the search. Default is `0`.
- `end` (optional): The ending byte position. Default is `-1`, which represents the end of the string.
- `BYTE|BIT` (optional): The unit to consider while searching. If not specified, `BYTE` is used.

## Return Values

The command returns the position (index) of the first occurrence of the specified bit (`0` or `1`).
If the bit is not found within the range, `-1` is returned.

## Code Examples

### Find the First `1` Bit

In this example, we will find the first occurrence of `1` in the string:

```shell
# String: example
# Hex:    0x65     0x78     0x61     0x6d     0x70     0x6c     0x65
# Binary: 01100101 01111000 01100001 01101101 01110000 01101100 01100101
dragonfly> SET mykey "example"
OK
dragonfly> BITPOS mykey 1
(integer) 1
```

The first occurrence of a `1` happens at bit position 1. (Remember, positions are zero-based).

### Find the First `0` Bit

Similarly, we can find the first occurrence of a `0` bit in the string:

```shell
dragonfly> SET mykey "example"
OK
dragonfly> BITPOS mykey 0
(integer) 0
```

In this case, the first occurrence of a `0` bit appears at position 0.

### Narrowing the Search with a Byte Range

We can specify a search range within bytes to limit the search. The following example looks for the first occurrence of `1` within the second and fourth bytes of the string:

```shell
# String: example
# Hex:    0x65     0x78     0x61     0x6d     0x70     0x6c     0x65
# Binary: 01100101 01111000 01100001 01101101 01110000 01101100 01100101
dragonfly> SET mykey "example"
OK
dragonfly> BITPOS mykey 1 1 3
(integer) 8
```

Here, we're telling the command to look only between the second and fourth bytes, and it finds the first `1` bit at position 8 (relative to the start of the string).

### Using `BITPOS` in a Packed Flag System

You can also use `BITPOS` in a system where flags are represented by bits within a packed binary string.

```shell
# Example binary string: 0x00 0x04 0x80
# Binary:                00000000 00000100 10000000
dragonfly> SET flags "\x00\x04\x80"
OK
dragonfly> BITPOS flags 1
(integer) 18
```

In this example, the first bit set to `1` is found at position 18.

## Best Practices

- Utilize `start` and `end` to limit your search to specific sections of the string, improving performance for larger strings.
- Use `BITPOS` when you need quick, efficient bit-level data scans without fully iterating through the data.

## Common Mistakes

- Forgetting that the result is a bit offset, not a byte offset, especially when interpreting the result.
- Assuming `BITPOS` modifies the string; it only performs a read and search operation.
- Specifying an invalid `bit` parameter (it must be either `0` or `1`).

## FAQs

### What happens if the key does not exist?

If the key does not exist, `BITPOS` returns `-1`, indicating that no result can be found in a non-existent key.

### Can I use negative indexes for the start and end parameters?

Yes, negative indexes are allowed, and they signify positions from the end of the string.

### How does the BYTE vs BIT mode work?

By default, `BITPOS` searches in `BYTE` mode, where each byte is processed sequentially.
However, specifying `BIT` tells the function to treat the string bit-by-bit in the search.
This mode is more granular and may be useful in certain low-level applications.

---
