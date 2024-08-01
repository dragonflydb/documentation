---
description: Discover how to handle string values as an array of bits with Redis BITFIELD.
---

import PageTitle from '@site/src/components/PageTitle';

# BITFIELD

<PageTitle title="Redis BITFIELD Explained (Better Than Official Docs)" />

## Introduction

The `BITFIELD` command in Redis is a versatile tool for manipulating string values at the bit level. It allows users to set, get, and perform arithmetic operations on specific bits within a string. This command is essential for tasks that require efficient storage and retrieval of binary data, such as implementing counters, flags, or compact data structures.

## Syntax

```plaintext
BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]
```

## Parameter Explanations

- **key**: The name of the Redis key.
- **GET**: Retrieves a specific bit field.
  - **type**: The type (e.g., `i8`, `u16`) specifying the bit width and signed/unsigned nature of the field.
  - **offset**: The zero-based bit position to start reading from.
- **SET**: Sets a specific bit field to a value.
  - **type**: The type specifying the bit width and signed/unsigned nature of the field.
  - **offset**: The zero-based bit position to start writing to.
  - **value**: The value to set in the specified bit field.
- **INCRBY**: Increments a specific bit field by a given amount.
  - **type**: The type specifying the bit width and signed/unsigned nature of the field.
  - **offset**: The zero-based bit position to start incrementing from.
  - **increment**: The amount to increment the bit field by.
- **OVERFLOW**: Specifies the overflow behavior for arithmetic operations. Can be `WRAP` (default), `SAT`, or `FAIL`.

## Return Values

- For **GET**: Returns the value of the requested bit field.
- For **SET**: Returns the previous value of the bit field.
- For **INCRBY**: Returns the new value of the bit field after incrementing.
- For **OVERFLOW**: Does not return a value directly but affects subsequent `INCRBY` operations.

#### Example Outputs

```cli
dragonfly> BITFIELD mykey GET u8 0
1) (integer) 5
```

```cli
dragonfly> BITFIELD mykey SET i8 1 127
1) (integer) 0
```

```cli
dragonfly> BITFIELD mykey INCRBY u16 0 5
1) (integer) 10
```

## Code Examples

### Basic Example

```cli
dragonfly> BITFIELD mykey SET u8 0 100
1) (integer) 0
dragonfly> BITFIELD mykey GET u8 0
1) (integer) 100
```

### Counter Implementation

Using `BITFIELD` to implement an 8-bit counter:

```cli
dragonfly> BITFIELD mycounter INCRBY u8 0 1
1) (integer) 1
dragonfly> BITFIELD mycounter INCRBY u8 0 1
1) (integer) 2
dragonfly> BITFIELD mycounter INCRBY u8 0 253
1) (integer) 255
dragonfly> BITFIELD mycounter INCRBY u8 0 1
1) (integer) 0  # Overflow occurs as it wraps around
```

### Flag Management

Using `BITFIELD` to manage multiple flags within a single key:

```cli
dragonfly> BITFIELD user_flags SET u1 0 1
1) (integer) 0
dragonfly> BITFIELD user_flags SET u1 1 1
1) (integer) 0
dragonfly> BITFIELD user_flags GET u1 0
1) (integer) 1
dragonfly> BITFIELD user_flags GET u1 1
1) (integer) 1
```

## Best Practices

- Use appropriate bit field types to save space and ensure correct arithmetic operations.
- Combine multiple operations in one `BITFIELD` command to improve performance.
- Be cautious with the `OVERFLOW` setting when performing arithmetic operations to avoid unexpected results.

## Common Mistakes

- Misalignment of bit offsets can lead to incorrect data manipulation.
- Forgetting to specify the correct type can cause unexpected behaviors, especially with signed vs. unsigned types.
- Not handling potential overflows properly when using `INCRBY`.

## FAQs

### What happens if I increment a bit field beyond its maximum value?

By default, the `INCRBY` operation will wrap around. You can change this behavior using the `OVERFLOW` sub
