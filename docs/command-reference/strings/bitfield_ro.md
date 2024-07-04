---
description: Master the use of Redis BITFIELD_RO for performing readonly bitfield operations.
---

import PageTitle from '@site/src/components/PageTitle';

# BITFIELD_RO

<PageTitle title="Redis BITFIELD_RO Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`BITFIELD_RO` is a read-only variant of the `BITFIELD` command in Redis. It is used to perform bit-level operations on strings without modifying them. This command is particularly useful for extracting specific bits or groups of bits from a string, which can be beneficial in scenarios where you need to read serialized data structures.

## Syntax

```
BITFIELD_RO key GET encoding offset [GET encoding offset ...]
```

## Parameter Explanations

- `key`: The key of the string value to operate on.
- `GET`: Specifies that the operation is read-only and will retrieve bits without modification.
- `encoding`: Defines the format and length of the bit field (e.g., `u8`, `i16`, etc.).
- `offset`: The position within the string where the bit field starts. This can be an integer or a relative position using `#`.

## Return Values

The command returns an array of integers, where each integer represents the result of a `GET` sub-command.

**Example Outputs:**

- `[5]`: Represents a single `GET` result.
- `[10, -3]`: Represents results from multiple `GET` operations.

## Code Examples

```cli
dragonfly> SET mykey "\x01\x02\x03\x04"
OK
dragonfly> BITFIELD_RO mykey GET u8 0
1) (integer) 1
dragonfly> BITFIELD_RO mykey GET u8 8
1) (integer) 2
dragonfly> BITFIELD_RO mykey GET i16 0
1) (integer) 258
dragonfly> BITFIELD_RO mykey GET u16 16
1) (integer) 772
```

## Best Practices

- Ensure that the offsets and encodings you specify align with the actual data structure stored in the string to avoid inconsistencies.
- Use `BITFIELD_RO` for reading purposes only. If you need to modify the bit fields, use the `BITFIELD` command instead.

## Common Mistakes

- Using `BITFIELD_RO` when intending to modify the string. Note that this command is strictly for read-only purposes.
- Incorrectly calculating offsets, especially when dealing with multi-byte encodings.

## FAQs

### What is the difference between BITFIELD and BITFIELD_RO?

`BITFIELD` can both read and modify bits in a string, whereas `BITFIELD_RO` is strictly read-only.

### Can I use BITFIELD_RO with non-string data types?

No, `BITFIELD_RO` operates only on strings. Attempting to use it on other data types will result in an error.

### What happens if the offset is out of range?

If the specified offset is beyond the length of the string, the command will return zero for those bit positions.
