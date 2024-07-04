---
description: Learn how to use Redis GETRANGE to get substrings from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETRANGE

<PageTitle title="Redis GETRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `GETRANGE` command in Redis is used to retrieve a substring of the value stored at a specific key. It's particularly useful when you need only a portion of a string rather than the entire value, such as extracting a specific segment of text or analyzing parts of a large string.

## Syntax

```plaintext
GETRANGE key start end
```

## Parameter Explanations

- **key**: The key of the string from which you want to get a range.
- **start**: The starting index of the range. This can be a positive or negative integer.
- **end**: The ending index of the range. This can also be a positive or negative integer.

  - Positive integers refer to positions from the beginning of the string (0-based index).
  - Negative integers refer to positions from the end of the string (-1 is the last character).

## Return Values

The `GETRANGE` command returns the specified substring of the string value stored at the given key. If the key does not exist, an empty string is returned.

## Code Examples

```cli
dragonfly> SET mykey "Hello, World!"
OK
dragonfly> GETRANGE mykey 0 4
"Hello"
dragonfly> GETRANGE mykey 7 -1
"World!"
dragonfly> GETRANGE mykey -6 -2
"World"
dragonfly> GETRANGE mykey 7 100
"World!"
```

## Best Practices

- To avoid errors, ensure that the specified key contains a string value before using `GETRANGE`.
- Be mindful of the indices used; specifying out-of-bound indices will not cause errors but will return data up to the available length.

## Common Mistakes

- Using `GETRANGE` on non-string keys, which will result in an error.
- Misinterpreting the negative indices; understanding that they count from the end of the string is crucial.
- Assuming indices beyond the string length might throw an error; instead, Redis adjusts and returns valid output within the string's bounds.

## FAQs

### What happens if I use `GETRANGE` on a non-existing key?

`GETRANGE` on a non-existing key returns an empty string.

### Can I use `GETRANGE` on binary or encoded data?

Yes, `GETRANGE` operates on the bytes of the string value, so it can be used on any string data, including binary or encoded data.
