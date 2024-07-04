---
description: Learn how to use Redis BITCOUNT to get the count of set bits in a string.
---

import PageTitle from '@site/src/components/PageTitle';

# BITCOUNT

<PageTitle title="Redis BITCOUNT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BITCOUNT` command in Redis is used to count the number of set bits (i.e., bits with value 1) in a string. This command is particularly useful in scenarios where you need to keep track of boolean states or binary data, such as feature flags, activity tracking, or compact storage of boolean arrays.

## Syntax

```
BITCOUNT key [start end]
```

## Parameter Explanations

- **key**: The key of the string for which you want to count the set bits.
- **start**: Optional. The starting byte position (inclusive). If not specified, it defaults to the beginning of the string.
- **end**: Optional. The ending byte position (inclusive). If not specified, it defaults to the end of the string.

## Return Values

The `BITCOUNT` command returns an integer representing the number of bits set to 1 in the specified range of the string.

### Example Outputs

- `(integer) 0`: No bits are set to 1.
- `(integer) 5`: Five bits are set to 1 within the specified range.

## Code Examples

```cli
dragonfly> SET mykey "\x01"  # Binary representation: 00000001
OK
dragonfly> BITCOUNT mykey
(integer) 1
dragonfly> SET mykey "\xFF"  # Binary representation: 11111111
OK
dragonfly> BITCOUNT mykey
(integer) 8
dragonfly> SET mykey "foobar"
OK
dragonfly> BITCOUNT mykey 0 3
(integer) 10
```

## Best Practices

- Use `BITCOUNT` for efficient bitwise operations, especially when dealing with large datasets that can be represented as binary strings.
- Combine `BITCOUNT` with other bitwise commands like `SETBIT`, `GETBIT`, and `BITOP` for comprehensive binary data manipulation.

## Common Mistakes

- Not considering the byte positions correctly when specifying the `start` and `end` parameters. This might lead to unexpected counts.
- Using `BITCOUNT` on non-string data types, which will result in an error.

## FAQs

### What happens if the specified key does not exist?

If the specified key does not exist, `BITCOUNT` will return 0 because there are no bits set in a nonexistent key.

### How does `BITCOUNT` handle negative indexes for `start` and `end`?

Negative indexes work similarly to Python slicing, where `-1` represents the last byte, `-2` the second-to-last, and so on.
