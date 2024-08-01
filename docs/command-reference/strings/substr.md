---
description: Learn how to use Redis SUBSTR to return a substring from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# SUBSTR

<PageTitle title="Redis SUBSTR Explained (Better Than Official Docs)" />

## Introduction

The `SUBSTR` command in Redis is used to extract a substring from a given string stored at a specified key. It's useful for retrieving parts of a string without fetching the entire value, which can save bandwidth and improve performance for large strings.

## Syntax

```plaintext
SUBSTR key start end
```

## Parameter Explanations

- **key**: The key holding the string value.
- **start**: The starting index of the substring (0-based). Negative values indicate offsets from the end of the string.
- **end**: The ending index of the substring. Negative values are supported.

## Return Values

The command returns the substring from the start to end indexes inclusive. If the key does not exist or if the specified range is out of bounds, an empty string is returned.

## Code Examples

### Basic Example

Extracting a basic substring from a string stored in Redis.

```cli
dragonfly> SET mystring "Hello, World!"
OK
dragonfly> SUBSTR mystring 0 4
"Hello"
dragonfly> SUBSTR mystring 7 11
"World"
```

### Extracting the Last Characters

Fetching the last few characters using negative indexing.

```cli
dragonfly> SET mystring "Hello, World!"
OK
dragonfly> SUBSTR mystring -6 -1
"World!"
```

### Using SUBSTR for Pagination

Simulate basic pagination by extracting substrings of fixed length.

```cli
dragonfly> SET longstring "This is a very long string used for testing."
OK
dragonfly> SUBSTR longstring 0 9
"This is a "
dragonfly> SUBSTR longstring 10 19
"very long "
dragonfly> SUBSTR longstring 20 29
"string use"
```

## Best Practices

- Use negative indices to simplify extraction from the end of strings.
- Ensure the start and end indices are within the valid range of the string length.

## Common Mistakes

- Misinterpreting 0-based indexing leading to off-by-one errors.
- Forgetting that negative indices count from the end of the string.

## FAQs

### What happens if the key doesn't exist?

The command will return an empty string if the key does not exist.

### How does SUBSTR handle out-of-range indices?

Out-of-range indices are trimmed to fit within the actual string length, and no error is thrown; an appropriate substring (or empty string) is returned.
