---
description: Learn how to use Redis SUBSTR to return a substring from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# SUBSTR

<PageTitle title="Redis SUBSTR Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SUBSTR` command in Redis is used to get a substring of the value stored at a specified key. It allows you to retrieve a segment of a string by specifying the start and end positions. This can be useful in scenarios where you need to parse or extract specific parts of a stored string without retrieving the entire value.

## Syntax

```plaintext
SUBSTR key start end
```

## Parameter Explanations

- **key**: The key holding the string value.
- **start**: The zero-based starting index of the substring.
- **end**: The zero-based ending index of the substring (inclusive).

## Return Values

The command returns the requested substring. If the specified key does not hold a string value, an error is returned. If the start or end indices are out of range, they will be adjusted to fit the actual length of the string.

### Examples:

- For a string "Hello, World!" with `start` as 0 and `end` as 4, the return value would be `"Hello"`.
- For a string "Hello, World!" with `start` as 7 and `end` as 11, the return value would be `"World"`.

## Code Examples

```cli
dragonfly> SET mystring "Hello, World!"
OK
dragonfly> SUBSTR mystring 0 4
"Hello"
dragonfly> SUBSTR mystring 7 11
"World"
dragonfly> SUBSTR mystring -5 -1
"orld!"
```

## Best Practices

When using the `SUBSTR` command, ensure the indices provided are within the bounds of the string length to avoid unnecessary adjustments. Using negative indices can help count positions from the end of the string, similar to Python slicing.

## Common Mistakes

- **Incorrect Indices**: Providing indices that are out of the range of the string's length can lead to unexpected results. Always validate your indices before using the command.
- **Wrong Data Type**: Attempting to use `SUBSTR` on a non-string key type will result in an error.

## FAQs

### What happens if I provide a negative index?

Negative indices are interpreted as counting from the end of the string. For example, `-1` represents the last character of the string.

### Can I use `SUBSTR` on binary data?

Yes, `SUBSTR` works on any string data, including binary data. Ensure your start and end indices appropriately reflect the sections of the binary data you wish to extract.

### Is `SUBSTR` zero-based?

Yes, the `start` and `end` parameters are zero-based indices.
