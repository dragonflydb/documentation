---
description: Master the use of Redis BITFIELD_RO for performing readonly bitfield operations.
---

import PageTitle from '@site/src/components/PageTitle';

# BITFIELD_RO

<PageTitle title="Redis BITFIELD_RO Explained (Better Than Official Docs)" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `BITFIELD_RO` command is a read-only variant of the `BITFIELD` command.
It allows you to query and retrieve specific bits or bitfields from a string without modifying the underlying string.
This command is useful for applications that need to interpret data stored as bitfields, such as compact representations of statuses or settings.

## Syntax

```plaintext
BITFIELD_RO key [GET encoding offset] ...
```

## Parameter Explanations

- `key`: The key of the string which is treated as a bitmap for read operations.
- `GET`: Subcommand used to specify the retrieval operation.
  - `encoding`: Specifies the format (bit width and signedness) of the bitfield to be retrieved, such as `i8`, `u16`, etc.
  - `offset`: The bit position within the string from which to start reading.

## Return Values

The command returns an array of integers, where each integer corresponds to the value of the retrieved bitfield according to the specified encoding.

## Code Examples

### Basic Example

Retrieve an unsigned 8-bit integer (starting at offset `0`) and a signed 16-bit integer (starting at offset `8`).

```shell
dragonfly> SET mystring "\x01\x02\x03"
OK
dragonfly> BITFIELD_RO mystring GET u8 0 GET i16 8
1) (integer) 1
2) (integer) 515
```

### Retrieving Multiple Bitfields

In this example, we extract multiple bitfields from a single string.
This demonstrates how to handle different offsets and encodings.

```shell
dragonfly> SET mystring "\xFF\xFE\xFD"
OK
dragonfly> BITFIELD_RO mystring GET u8 0 GET u8 8 GET i16 16
1) (integer) 255
2) (integer) 254
3) (integer) -3
```

### Working with Larger Fields

Extracting larger bitfields, such as 32-bit integers, to demonstrate handling of wider data.

```shell
dragonfly> SET mystring "\x00\x00\x00\x01\x00\x00\x00\x02"
OK
dragonfly> BITFIELD_RO mystring GET u32 0 GET u32 32
1) (integer) 1
2) (integer) 2
```

## Best Practices

- Use appropriate encodings (`u8`, `i16`, etc.) to match the data you expect to retrieve.
- Align your offsets correctly to avoid unexpected values due to partial byte reads.

## Common Mistakes

- Incorrectly specifying offsets can lead to unexpected results. Ensure that offsets correctly align with the bit widths of the fields being read.
- Mixing up signed (`i`) and unsigned (`u`) encodings may produce incorrect values when interpreting the data.

## FAQs

### Can `BITFIELD_RO` modify the string?

No, `BITFIELD_RO` is strictly read-only and cannot modify the underlying string.

### What happens if I use an offset that exceeds the length of the string?

If the specified offset extends beyond the end of the string, `BITFIELD_RO` will return `nil` for that field.
