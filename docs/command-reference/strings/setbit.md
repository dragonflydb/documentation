---
description: Learn about Redis SETBIT to manipulate specific binary bits of a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# SETBIT

<PageTitle title="Redis SETBIT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SETBIT` command in Redis is used to set or clear the bit at a specified offset in the string value stored at a key. It's typically used for bit manipulation tasks, such as managing bitmap indices, feature flags, or tracking user activity.

## Syntax

```
SETBIT key offset value
```

## Parameter Explanations

- `key`: The name of the key where the string value is stored.
- `offset`: The position (starting from 0) within the string to set or clear the bit.
- `value`: The bit value to set, which must be either 0 or 1.

## Return Values

`SETBIT` returns the original bit value stored at the specified offset before it was set.

### Examples:

1. Setting a new bit:

   - If the bit was originally 0: `(integer) 0`
   - If the bit was originally 1: `(integer) 1`

2. Clearing a bit:
   - If the bit was originally 0: `(integer) 0`
   - If the bit was originally 1: `(integer) 1`

## Code Examples

```cli
dragonfly> SETBIT mykey 7 1
(integer) 0

dragonfly> SETBIT mykey 7 0
(integer) 1

dragonfly> SETBIT mykey 7 1
(integer) 0

dragonfly> GETBIT mykey 7
(integer) 1
```

## Best Practices

When working with large offsets, ensure that memory usage is controlled, as setting a high offset can lead to increased memory consumption.

## Common Mistakes

- Using non-integer values for `offset`.
- Setting `value` to anything other than 0 or 1, which will result in an error.

## FAQs

### What happens if the key does not exist?

If the key does not exist, it is treated as a zero-length string, so `SETBIT` will extend it as needed and initialize unspecified bits to 0.

### Can I use negative offsets?

No, the `offset` parameter must be a non-negative integer.
