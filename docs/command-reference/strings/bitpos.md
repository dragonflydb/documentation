---
description: Discover how to find the position of a bit set to 1 or 0 in a string with Redis BITPOS.
---

import PageTitle from '@site/src/components/PageTitle';

# BITPOS

<PageTitle title="Redis BITPOS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BITPOS` command in Redis is used to find the position of the first bit set to 1 or 0 in a string. It's particularly useful in scenarios where you need to quickly locate a specific bit within a binary string, such as finding the first occurrence of an event in a bitmap.

## Syntax

```
BITPOS key bit [start] [end]
```

## Parameter Explanations

- **key**: The name of the key holding the string value.
- **bit**: The bit value to search for (must be 0 or 1).
- **start** (optional): The start index of the search range (inclusive). Defaults to 0 if not provided.
- **end** (optional): The end index of the search range (inclusive). If not specified, the search goes until the end of the string.

## Return Values

- Returns the position of the first bit set to the specified value.
- If no matching bit is found, it returns -1.

### Examples

1. If the bit exists:

   ```cli
   dragonfly> SET mykey "\x00\x00\x00\xff"
   OK
   dragonfly> BITPOS mykey 1
   (integer) 24
   ```

2. If the bit does not exist:

   ```cli
   dragonfly> SET mykey "\xff\xf0\x00"
   OK
   dragonfly> BITPOS mykey 0 0 1
   (integer) 12
   ```

3. When specifying a range:
   ```cli
   dragonfly> SET mykey "\x00\xff\x00"
   OK
   dragonfly> BITPOS mykey 1 1 2
   (integer) 8
   ```

## Code Examples

```cli
dragonfly> SET mybitmap "\x00\xff\xf0"
OK
dragonfly> BITPOS mybitmap 1
(integer) 8
dragonfly> BITPOS mybitmap 0 1
(integer) 16
dragonfly> BITPOS mybitmap 1 2
(integer) 20
dragonfly> BITPOS mybitmap 0 0 1
(integer) 0
```

## Common Mistakes

- **Invalid Bit Values**: Using values other than 0 or 1 for the bit parameter will result in an error.
  ```cli
  dragonfly> BITPOS mybitmap 2
  (error) ERR bit must be 0 or 1
  ```
- **Out of Range Indexes**: Specifying a start or end index outside the actual length of the string leads to incorrect results.

## FAQs

### What happens if the key does not exist?

If the key doesn't exist, `BITPOS` returns -1 because there are no bits to search through.

### Can BITPOS handle large strings efficiently?

Yes, `BITPOS` is optimized for efficiency even with large strings, making it suitable for scenarios involving large bitmaps or binary data.
