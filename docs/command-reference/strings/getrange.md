---
description: Learn how to use Redis GETRANGE to get substrings from a string value.
---

import PageTitle from '@site/src/components/PageTitle';

# GETRANGE

<PageTitle title="Redis GETRANGE Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `GETRANGE` command is used to retrieve a substring from a string stored at a specific key.
It allows you to extract characters from the stored string by specifying the starting and ending offsets (**both inclusive**), based on **byte positions**.
This is a useful tool when you want portions of a string without fetching the entire value.

## Syntax

```shell
GETRANGE key start end
```

- **Time complexity:** O(N) where N is the length of the returned string.
  The complexity is ultimately determined by the returned length, but because creating a substring from an existing string is very cheap, it can be considered O(1) for small strings.
- **ACL categories:** @read, @string, @slow

## Parameter Explanations

- `key`: The key that holds the string from which you want to extract a substring.
- `start`: The starting character position (zero-based index) in the string.
- `end`: The ending character position (**inclusive**) for the substring, or `-1` to refer to the last character.

## Return Values

The command returns the specified substring extracted from the string value stored at the specified key.

## Code Examples

### Basic Example

Retrieve a substring from a stored string:

```shell
dragonfly$> SET mykey "example"
OK
dragonfly$> GETRANGE mykey 0 2
"exa"
```

In the above example, the substring `exa` is returned as it starts from index `0` and ends at index `2`.

### Extract Substring Using Negative Index

You can use negative numbers to address characters starting from the end:

```shell
dragonfly$> SET mykey "example"
OK
dragonfly$> GETRANGE mykey -4 -1
"mple"
```

In this case, `-4` refers to the fourth character from the end, and `-1` refers to the last character.

### Extract a Substring in a Range That Does Not Fully Exist

If the given range exceeds the string's length, the command will still return what is available:

```shell
dragonfly$> SET mykey "example"
OK
dragonfly$> GETRANGE mykey 5 50
"le"
```

Here, although the ending index is beyond the actual string length, Dragonfly returns up to the last available characters, which is the `le` substring.

### Use Case for Handling Large Strings

For user data like URLs, session identifiers, or logs, you may want to extract meaningful segments without loading the entire dataset:

```shell
dragonfly$> SET logentry "ErrorCode:404,Page:/about,Message:Not Found,ClientIP:192.168.1.50"
OK
dragonfly$> GETRANGE logentry 11 24
"404,Page:/about"
```

This allows you to fetch specific parts of user data efficiently.

## Best Practices

- Use `GETRANGE` when dealing with large strings to minimize memory consumption and bandwidth by fetching only what you need.
- Negative indices are a powerful feature but ensure that they accurately reflect the part of the string you're interested in.

## Common Mistakes

- Providing out-of-bound indexes does not throw an error, but can lead to unexpected results. Make sure your range matches the string structure.
- Confusing character positions with byte positions in certain cases, especially with non-ASCII data, may lead to inaccuracies.

## FAQs

### What happens if the key does not exist?

If the key does not exist, `GETRANGE` will return an empty string.

### How does `GETRANGE` handle out-of-bound indices?

If the provided `start` or `end` indices are out-of-bound (e.g., larger than the string length), the command simply returns as much of the string as falls within the valid range.
It does not raise an error for out-of-bound indices.

### How does `GETRANGE` handle encoding?

`GETRANGE` operates at the character level for ASCII-compatible encoding, but with multibyte encodings (like UTF-8), ranges refer to **byte positions** rather than actual characters.

### Can I use `GETRANGE` on binary data?

Yes, `GETRANGE` works on strings, whether they are text or binary. The start and end positions relate to bytes when dealing with binary data.
