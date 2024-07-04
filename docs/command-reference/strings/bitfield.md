---
description: Discover how to handle string values as an array of bits with Redis BITFIELD.
---

import PageTitle from '@site/src/components/PageTitle';

# BITFIELD

<PageTitle title="Redis BITFIELD Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BITFIELD` command in Redis manipulates string values representing binary data at the bit level. This command is useful for managing compact data structures like bitmap indices, counters, or storing flags and other binary state information.

## Syntax

```
BITFIELD key [GET type offset] [SET type offset value] [INCRBY type offset increment] [OVERFLOW WRAP|SAT|FAIL]
```

## Parameter Explanations

- **key**: The key of the string to manipulate.
- **GET type offset**: Reads a value from the string.
  - **type**: The type of the value (e.g., i8, u8, i16, u16, etc.).
  - **offset**: Bit position from where to read the value.
- **SET type offset value**: Sets a value in the string.
  - **value**: The value to set.
- **INCRBY type offset increment**: Increments a value by a given amount.
  - **increment**: The amount to increment.
- **OVERFLOW WRAP|SAT|FAIL**: Defines the overflow behavior for INCRBY operations.

## Return Values

- **GET** returns the specified value.
- **SET** returns the previous value stored at the given offset.
- **INCRBY** returns the new incremented value.
- **OVERFLOW** does not return anything directly but affects subsequent INCRBY.

## Code Examples

```cli
dragonfly> BITFIELD mykey SET u8 0 100
1) (integer) 0
dragonfly> BITFIELD mykey GET u8 0
1) (integer) 100
dragonfly> BITFIELD mykey INCRBY u8 0 10
1) (integer) 110
dragonfly> BITFIELD mykey OVERFLOW SAT
"OK"
dragonfly> BITFIELD mykey INCRBY u8 0 200
1) (integer) 255
dragonfly> BITFIELD mykey GET u8 0
1) (integer) 255
```

## Best Practices

- Define the expected range of your data when using types like u8, i16, etc., to avoid unexpected results.
- Combine multiple subcommands in one `BITFIELD` call to optimize performance.

## Common Mistakes

- Misinterpreting the offset as byte-level instead of bit-level.
- Forgetting to set the overflow policy, leading to undesired wraparounds.

## FAQs

### What happens if I don't set an overflow policy?

If no overflow policy is set, the default WRAP behavior will be used.

### Can I use negative offsets?

Yes, negative offsets count from the end of the string.
