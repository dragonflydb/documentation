---
description: Understand how Redis GETBIT retrieves a specific bit from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETBIT

<PageTitle title="Redis GETBIT Explained (Better Than Official Docs)" />

## Introduction

The `GETBIT` command in Redis is used to return the bit value at a specified offset within a string stored at a given key. This command is particularly useful for bit manipulation operations such as implementing bloom filters, tracking user activity, or managing feature flags.

## Syntax

```
GETBIT key offset
```

## Parameter Explanations

- **key**: The key of the string where the bit will be fetched.
- **offset**: The position in the string to retrieve the bit from. The offset starts at 0.

## Return Values

- Returns the bit value (0 or 1) stored at the specified offset.
- If the offset is beyond the string length, it returns 0.

Example outputs:

- `(integer) 0`
- `(integer) 1`

## Code Examples

### Basic Example

```cli
dragonfly> SET mystring "a"
OK
dragonfly> GETBIT mystring 6
(integer) 1
dragonfly> GETBIT mystring 7
(integer) 0
```

### Feature Flag Management

This example demonstrates how to use `GETBIT` for managing feature flags in an application.

```cli
# Enable a feature flag at bit position 2
dragonfly> SETBIT features 2 1
(integer) 0
# Check if the feature flag is enabled
dragonfly> GETBIT features 2
(integer) 1
# Check if another feature flag is enabled at bit position 5
dragonfly> GETBIT features 5
(integer) 0
```

### User Activity Tracking

Use `GETBIT` to track daily user activity by using bits to represent days of the month.

```cli
# Assume we already have some activity recorded for user:1234
dragonfly> SETBIT user:1234:activity 0 1 # Day 1
(integer) 0
dragonfly> SETBIT user:1234:activity 1 1 # Day 2
(integer) 0

# Check user activity on day 3 (should be inactive)
dragonfly> GETBIT user:1234:activity 2
(integer) 0

# Check user activity on day 1 (should be active)
dragonfly> GETBIT user:1234:activity 0
(integer) 1
```

### Implementing a Bloom Filter

Bloom filters are space-efficient probabilistic data structures used to test whether an element is in a set. In this example, `GETBIT` is used to check the presence of an element.

```cli
# Assume a Bloom filter with bits set at positions derived from hash functions
dragonfly> SETBIT bloomfilter 100 1
(integer) 0
dragonfly> SETBIT bloomfilter 200 1
(integer) 0

# Check the bit at a specific position to see if the element might be present
dragonfly> GETBIT bloomfilter 100
(integer) 1
dragonfly> GETBIT bloomfilter 300
(integer) 0
```

## Best Practices

- Use appropriate data structures and offsets to avoid excessive memory usage.
- Combine `GETBIT` with other bitwise commands (`SETBIT`, `BITCOUNT`) to perform complex bit-level operations efficiently.

## Common Mistakes

- Accessing offsets that are too large can lead to unexpected results; ensure offsets are within the valid range of the string's length.
- Misinterpreting the zero-based offset can lead to off-by-one errors.
