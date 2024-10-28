---
description: Learn how to use Redis SUBSTR to return a substring from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# SUBSTR

<PageTitle title="Redis SUBSTR Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `SUBSTR` command is used to retrieve a substring from a string stored at a specific key.
It allows you to extract characters from the stored string by specifying the starting and ending offsets (**both inclusive**), based on **byte positions**.
This is a useful tool when you want portions of a string without fetching the entire value.

`SUBSTR` is equivalent to the [`GETRANGE`](getrange.md) command.
When migrating or writing new code, it is recommended to use [`GETRANGE`](getrange.md) instead of `SUBSTR` for better readability and naming consistency.

## Syntax

```shell
SUBSTR key start end
```

- **Time complexity:** O(N) where N is the length of the returned string.
  The complexity is ultimately determined by the returned length, but because creating a substring from an existing string is very cheap, it can be considered O(1) for small strings.
- **ACL categories:** @read, @string, @slow

## Parameter Explanations

- `key`: The key in which the string value is stored.
- `start`: The starting index (zero-based) for the substring.
  A negative `start` value can be used to offset from the end of the string.
- `end`: The end index (**inclusive**) for the substring.
  A negative `end` value can be used to offset from the end of the string.

## Return Values

The command returns the substring specified by the start and end positions.

## Code Examples

### Basic Example

Extract a substring from an entire string:

```shell
dragonfly> SET mykey "example"
OK
dragonfly> SUBSTR mykey 0 6
"example"
```

### Extract Substring with Start and End Indices

Extract a substring from the second to the sixth character:

```shell
dragonfly> SET mykey "example"
OK
dragonfly> SUBSTR mykey 1 5
"xampl"
```

### Negative Indices for Start and End

You can use negative numbers to specify positions relative to the string's end.

For instance, the positions `-2` and `-1` refer to the second-to-last and the last characters, respectively:

```shell
dragonfly> SET mykey "example"
OK
dragonfly> SUBSTR mykey -2 -1
"le"
```

### Handling Non-Existing Characters

If the specified range goes out of bounds, `SUBSTR` will return only the portion of the string up to its maximum length:

```shell
dragonfly> SET mykey "example"
OK
dragonfly> SUBSTR mykey 4 100
"ple"
```

## Best Practices

- If you need to extract a portion of a string based on indices, `SUBSTR` (or [`GETRANGE`](getrange.md)) is a useful and efficient command.
- Use negative indices when you want to refer to characters from the end of the string, making it easier to work with dynamic or variable-length string values.
- For more complex string manipulations, combining different string commands like [`SET`](set.md), [`APPEND`](append.md), and `SUBSTR` can be a powerful approach.

## Common Mistakes

- Forgetting that **both `start` and `end` indices are inclusive**. Always check that your end index is what you expect when specifying the range.
- Providing out-of-bound indexes does not throw an error, but can lead to unexpected results. Make sure your range matches the string structure.
- Confusing character positions with byte positions in certain cases, especially with non-ASCII data, may lead to inaccuracies.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `SUBSTR` behaves as if the value were an empty string and returns an empty string.

### How does `SUBSTR` handle out-of-bound indices?

If the provided `start` or `end` indices are out-of-bound (e.g., larger than the string length), the command simply returns as much of the string as falls within the valid range.
It does not raise an error for out-of-bound indices.
