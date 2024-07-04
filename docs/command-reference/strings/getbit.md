---
description: Understand how Redis GETBIT retrieves a specific bit from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETBIT

<PageTitle title="Redis GETBIT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GETBIT` command in Redis is used to return the bit value at an offset in a string. This command is particularly useful for implementing bitmaps or dealing with binary data efficiently. Typical use cases include tracking user activity, implementing feature flags, and managing binary states.

## Syntax

```cli
GETBIT key offset
```

## Parameter Explanations

- `key`: The name of the key containing the string.
- `offset`: The position of the bit you want to retrieve, starting from 0.

## Return Values

The `GETBIT` command returns the bit value stored at the specified offset. The possible outputs are:

- `0`: If the bit at the specified offset is not set (or if the bit does not exist).
- `1`: If the bit at the specified offset is set.

## Code Examples

```cli
dragonfly> SET mykey "a"        # 'a' in binary is 01100001
OK

dragonfly> GETBIT mykey 1       # Get the bit at offset 1
(integer) 1

dragonfly> GETBIT mykey 2       # Get the bit at offset 2
(integer) 1

dragonfly> GETBIT mykey 3       # Get the bit at offset 3
(integer) 0

dragonfly> GETBIT mykey 7       # Get the bit at offset 7
(integer) 1

dragonfly> GETBIT mykey 8       # Offset 8 doesn't exist in this context
(integer) 0
```

## Best Practices

- Ensure that the `offset` parameter is within the bounds of your string data to avoid unnecessary operations.
- Use `GETBIT` in combination with `SETBIT` to efficiently manage and query bitmap data.

## Common Mistakes

- Using a negative offset: Offsets must be non-negative integers.
- Expecting a non-binary response: `GETBIT` will always return `0` or `1`.

## FAQs

### What happens if I query an offset beyond the length of the string?

Redis will treat any out-of-bound offsets as zeros. For example, querying an offset of 1000 on a short string will return `0`.

### Can `GETBIT` be used on non-string types?

No, `GETBIT` works exclusively with string values. Attempting to use it on other data types will result in an error.
