---
description: Learn how to use Redis GETRANGE to get substrings from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETRANGE

<PageTitle title="Redis GETRANGE Explained (Better Than Official Docs)" />

## Introduction

The `GETRANGE` command in Redis is used to retrieve a substring of the value stored at a specified key. This command is beneficial when you need to extract specific portions of data from a string without fetching the entire string from the database. It's particularly efficient for working with large strings where only a portion of the information is needed.

## Syntax

```cli
GETRANGE key start end
```

## Parameter Explanations

- **key**: The name of the key holding the string.
- **start**: The zero-based start index of the substring (inclusive).
- **end**: The zero-based end index of the substring (inclusive). Use -1 to specify the last character.

## Return Values

Returns the substring extracted from the value stored at the given key, corresponding to the specified range.

### Examples

- Extracting a substring from a string value:

  ```cli
  dragonfly> SET mykey "This is a string"
  OK
  dragonfly> GETRANGE mykey 0 3
  "This"
  ```

- Using negative indices:
  ```cli
  dragonfly> GETRANGE mykey -6 -1
  "string"
  ```

## Code Examples

### Basic Example

Extract the first four characters from a string:

```cli
dragonfly> SET mykey "Hello, world!"
OK
dragonfly> GETRANGE mykey 0 4
"Hello"
```

### Retrieving Part of a Log Entry

Suppose you store log entries as strings and want to extract a specific segment:

```cli
dragonfly> SET log_entry "2024-07-26 12:34:56 ERROR An error occurred"
OK
# Extract the timestamp
dragonfly> GETRANGE log_entry 0 19
"2024-07-26 12:34:56"
```

### Parsing Fixed-Width Data Files

If you have a fixed-width format file stored as a single string, you can retrieve specific fields by their positions:

```cli
dragonfly> SET record "1234567890John Doe    40000"
OK
# Extract the ID
dragonfly> GETRANGE record 0 9
"1234567890"
# Extract the name
dragonfly> GETRANGE record 10 18
"John Doe"
# Extract the salary
dragonfly> GETRANGE record 19 23
"40000"
```

## Best Practices

When using `GETRANGE`, ensure the indices are within the bounds of the string length to avoid unexpected empty results. Utilize this command for optimizing performance by retrieving only necessary data segments instead of whole values.

## Common Mistakes

- **Incorrect Indices**: Specifying an out-of-bound range will return an empty string rather than producing an error.
  ```cli
  dragonfly> GETRANGE mykey 50 60
  ""
  ```

## FAQs

### What happens if the `start` index is larger than the `end` index?

If the `start` index is greater than the `end` index, `GETRANGE` will return an empty string.

### Can I use negative indices with `GETRANGE`?

Yes, negative indices can be used to specify offsets from the end of the string. For example, `-1` refers to the last character.
