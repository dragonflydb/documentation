---
description: Learn how to conduct bitwise operations on strings using Redis BITOP.
---

import PageTitle from '@site/src/components/PageTitle';

# BITOP

<PageTitle title="Redis BITOP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BITOP` command in Redis performs bitwise operations between strings stored at specified keys and stores the result in a destination key. Typical use cases include manipulating binary data, performing fast aggregations on sets of flags, or implementing efficient counters.

## Syntax

```
BITOP operation destkey key [key ...]
```

## Parameter Explanations

- **operation**: The bitwise operation to perform. Possible values are:
  - `AND`: Perform a bitwise AND.
  - `OR`: Perform a bitwise OR.
  - `XOR`: Perform a bitwise XOR.
  - `NOT`: Perform a bitwise NOT (only takes one source key).
- **destkey**: The key where the result will be stored.
- **key [key ...]**: One or more source keys which hold the strings to operate on.

## Return Values

The `BITOP` command returns the length of the string stored in the destination key, which is equal to the length of the longest input string.

### Examples

```shell
dragonfly> SET key1 "\x01"
OK
dragonfly> SET key2 "\x01"
OK
dragonfly> BITOP AND destkey key1 key2
(integer) 1
dragonfly> GET destkey
"\x01"

dragonfly> SET key3 "\x02"
OK
dragonfly> BITOP OR destkey key1 key3
(integer) 1
dragonfly> GET destkey
"\x03"

dragonfly> BITOP XOR destkey key1 key3
(integer) 1
dragonfly> GET destkey
"\x03"
```

## Best Practices

- Ensure that the keys involved contain binary-safe strings.
- Use the smallest possible number of keys to avoid unnecessary memory usage and processing time.

## Common Mistakes

- Using non-existent keys in the operation can yield unexpected results since Redis treats missing keys as empty strings.
- Incorrectly assuming `BITOP NOT` supports multiple keys; it only supports a single source key.

## FAQs

### What happens if the keys have different lengths?

Redis pads the shorter strings with zero-bytes so all strings are treated as having the same length as the longest string involved in the operation.

### Can I perform `BITOP` on non-binary string values?

Yes, but make sure the values are interpreted as binary by your application logic. `BITOP` works at the byte level, regardless of the actual content.
