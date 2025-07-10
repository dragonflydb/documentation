---
description: Learn how to use Redis STRLEN to get the length of the string stored in a key.
---

import PageTitle from '@site/src/components/PageTitle';

# STRLEN

<PageTitle title="Redis STRLEN Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `STRLEN` command is used to get the number of bytes in a string value stored at a given key.
This command is useful when you want to measure the length of a string,
for example when validating input length or when you need to allocate storage based on string size.

## Syntax

```shell
STRLEN key
```

- **Time complexity:** O(1)
- **ACL categories:** @read, @string, @fast

## Parameter Explanations

- `key`: The key of the string for which the length is calculated.

## Return Values

The command returns an integer representing the length of the string, in bytes.

## Code Examples

### Basic Example

Get the length of a string:

```shell
dragonfly$> SET mykey "Dragonfly"
OK
dragonfly$> STRLEN mykey
(integer) 9
```

### Length of an Empty String

If the string is an empty string, return `0`:

```shell
dragonfly$> SET mykey ""
OK
dragonfly$> STRLEN mykey
(integer) 0
```

### `STRLEN` on Non-Existent Keys

When the key does not exist, `STRLEN` will return `0`:

```shell
dragonfly$> STRLEN non_existent_key
(integer) 0
```

### Using `STRLEN` with Multibyte Characters

Bear in mind that `STRLEN` returns the length in **bytes**, not characters.
For example, a string with multibyte characters will have a byte length that may differ from its character count:

```shell
dragonfly$> SET mykey "你好"
OK
dragonfly$> STRLEN mykey
(integer) 6  # Most Chinese characters require 3 bytes each in UTF-8 encoding.
```

## Best Practices

- Use `STRLEN` to check the byte size of string values before performing operations that might depend on their length.
- Be aware that for multibyte character encodings (like UTF-8), the byte size might not be equivalent to the number of characters in the string.

## Common Mistakes

- Confusing string length in characters with string length in bytes.
  Remember, `STRLEN` returns the byte length, which may vary for strings containing multibyte characters.
- Assuming `STRLEN` will throw an error for non-existent keys. In fact, it simply returns `0` in such cases.

## FAQs

### What happens if the string contains multibyte characters?

`STRLEN` measures the string length in bytes, not in characters.
So if your string contains multibyte characters, such as emojis or characters from non-Latin alphabets like Chinese, the byte size will be higher than the number of characters.

### What if the key stores a non-string data type?

If the value stored at the key is not a string (e.g., a list, set, or hash), `STRLEN` will return an error.
You should ensure the key holds a string value before using this command.
