---
description: Discover how to find the position of a bit set to 1 or 0 in a string with Redis BITPOS.
---

import PageTitle from '@site/src/components/PageTitle';

# BITPOS

<PageTitle title="Redis BITPOS Explained (Better Than Official Docs)" />

## Introduction

The `BITPOS` command in Redis is used to find the first bit set to 1 or 0 in a string, starting from a specified position. This command is particularly useful for efficiently locating specific bits within large binary data sets.

## Syntax

```cli
BITPOS key bit [start] [end] [BYTE|BIT]
```

## Parameter Explanations

- **key**: The key of the string you are examining.
- **bit**: The bit value to search for (either 0 or 1).
- **start** (optional): The starting byte offset to begin searching. Defaults to the beginning of the string.
- **end** (optional): The ending byte offset to end the search. Defaults to the end of the string.
- **BYTE|BIT** (optional): Specifies whether offsets are expressed in bytes or bits. Defaults to bytes if not specified.

## Return Values

Returns the position of the first bit set to the specified value (0 or 1). If no match is found, it returns -1.

### Examples:

- When searching for the first `1` bit:

  ```cli
  (integer) 4
  ```

- When no matching bit is found:
  ```cli
  (integer) -1
  ```

## Code Examples

### Basic Example

Finding the first occurrence of bit `1`:

```cli
dragonfly> SET mykey "\x00\x00\x00\x09"
OK
dragonfly> BITPOS mykey 1
(integer) 27
```

### Finding a Specific Bit Within a Range

Let's say you want to find the first `0` bit between byte positions 1 and 3:

```cli
dragonfly> SET mykey "\xff\xf0\x00"
OK
dragonfly> BITPOS mykey 0 1 2
(integer) 12
```

### Using BYTE vs BIT Offset

By default, `start` and `end` are byte offsets. To use bit offsets instead, specify `BIT`:

```cli
dragonfly> SET mykey "\x00\xff\xf0"
OK
dragonfly> BITPOS mykey 1 0 20 BIT
(integer) 8
```

## Best Practices

- Use `BITPOS` with explicit ranges to limit the search scope, especially on very large keys.
- Combine `BITPOS` with other bitwise operations like `GETBIT` and `SETBIT` for more complex bit manipulation tasks.

## Common Mistakes

- Forgetting that the default offsets are in bytes, not bits. Always specify `BIT` if you need bit-level precision.
- Not accounting for the possibility of a `-1` return value when no matching bit is found.

## FAQs

### What happens if the string does not contain the specified bit?

`BITPOS` will return `-1` if it doesn't find the specified bit within the given range.

### Can I search for a bit across specific byte ranges?

Yes, by providing the `start` and `end` parameters, you can limit the search to specific byte ranges.
