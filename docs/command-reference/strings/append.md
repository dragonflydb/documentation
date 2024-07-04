---
description: Learn to extend a string value in Redis using the APPEND command.
---

import PageTitle from '@site/src/components/PageTitle';

# APPEND

<PageTitle title="Redis APPEND Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `APPEND` command in Redis is used to append a value to the end of an existing string key. If the key does not exist, it creates the key with the given value. This command is particularly useful for logging or accumulating text data without overwriting the existing content.

## Syntax

```plaintext
APPEND key value
```

## Parameter Explanations

- `key`: The name of the string key to which the value will be appended. If the key doesn't exist, it will be created.
- `value`: The string value that you want to append to the existing value of the key.

## Return Values

The `APPEND` command returns the total length of the string after the append operation.

### Examples of possible outputs:

- If the initial value of the key is "Hello" and you append ", World!", the return value will be `13` because the resulting string "Hello, World!" has 13 characters.

## Code Examples

```cli
dragonfly> SET mykey "Hello"
OK
dragonfly> APPEND mykey ", World!"
(integer) 13
dragonfly> GET mykey
"Hello, World!"
dragonfly> APPEND mykey " How are you?"
(integer) 24
dragonfly> GET mykey
"Hello, World! How are you?"
```

## Best Practices

- Ensure that the key you're appending to is intended to be a string. Using `APPEND` on non-string keys will result in a type error.
- Use `APPEND` in scenarios where continuous accumulation of text data is required, such as logging messages or building simple reports.

## Common Mistakes

- Trying to append using non-string keys. This will generate an error since `APPEND` only works with string keys.
- Not checking the length of the string after multiple append operations, which could lead to the string becoming very large and potentially impacting performance.

## FAQs

### What happens if the key does not exist?

If the key does not exist, the `APPEND` command will create a new key with the specified value.

### Can I use `APPEND` with other data types like lists or hashes?

No, `APPEND` is specifically designed for string values. Using it with other data types will result in an error.
