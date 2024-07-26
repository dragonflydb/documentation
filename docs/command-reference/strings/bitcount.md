---
description: Learn how to use Redis BITCOUNT to get the count of set bits in a string.
---

import PageTitle from '@site/src/components/PageTitle';

# BITCOUNT

<PageTitle title="Redis BITCOUNT Explained (Better Than Official Docs)" />

## Introduction

`BITCOUNT` is a Redis command used to count the number of set bits (i.e., bits with value 1) in a string. It is particularly useful for efficiently performing bitwise operations and can be used in scenarios like tracking user activity, feature flags, or implementing bloom filters.

## Syntax

```plaintext
BITCOUNT key [start end]
```

## Parameter Explanations

- `key`: The key of the string where bits are counted.
- `start` (optional): The starting byte position to count the bits. Default is 0.
- `end` (optional): The ending byte position to count the bits. Default is -1, indicating the end of the string.

## Return Values

The command returns an integer representing the number of bits set to 1 within the specified range.

### Examples

```cli
dragonfly> SET mykey "foobar"
OK
dragonfly> BITCOUNT mykey
(integer) 26
dragonfly> BITCOUNT mykey 0 0
(integer) 4
dragonfly> BITCOUNT mykey 1 1
(integer) 6
```

## Code Examples

### Basic Example

Count all set bits in a string:

```cli
dragonfly> SET mykey "example"
OK
dragonfly> BITCOUNT mykey
(integer) 29
```

### Count Bits in a Specific Range

Count bits from the second to the fourth byte:

```cli
dragonfly> SET mykey "example"
OK
dragonfly> BITCOUNT mykey 1 3
(integer) 11
```

### Using BITCOUNT for Feature Flags

Imagine you have a feature flag system where each bit represents whether a feature is enabled (1) or disabled (0) for different users:

```cli
dragonfly> SET features "\x01\x02\x04"  # Binary: 00000001 00000010 00000100
OK
dragonfly> BITCOUNT features
(integer) 3  # Three features are enabled across different users
```

## Best Practices

- When working with large strings, consider specifying start and end parameters to limit the scope and improve performance.
- Use BITCOUNT for low-level bitwise operations where you need efficient storage and quick bit checks.

## Common Mistakes

- Forgetting that `start` and `end` parameters are byte offsets, not bit offsets.
- Assuming BITCOUNT modifies the string; it only reads and counts the bits.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `BITCOUNT` returns 0.

### Can I use negative indexes for the start and end parameters?

Yes, similar to other Redis commands, negative indexes can be used to count bits from the end of the string.
