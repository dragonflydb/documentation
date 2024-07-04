---
description: Learn how to use Redis STRLEN to get the length of the string stored in a key.
---

import PageTitle from '@site/src/components/PageTitle';

# STRLEN

<PageTitle title="Redis STRLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `STRLEN` command in Redis is used to get the length of the value stored in a key. This command is particularly useful when you need to determine the size of a string value before processing it, or to ensure that a value does not exceed a certain length.

## Syntax

```plaintext
STRLEN key
```

## Parameter Explanations

- **key**: The key whose value's length you want to retrieve. It should be a string type. If the key does not exist, `STRLEN` returns 0.

## Return Values

The `STRLEN` command returns an integer representing the length of the string stored at the specified key.

Example outputs:

- If the key exists and has a value: `(integer) <length>`
- If the key does not exist: `(integer) 0`

## Code Examples

```cli
dragonfly> SET mykey "Hello, world!"
OK
dragonfly> STRLEN mykey
(integer) 13
dragonfly> STRLEN non_existent_key
(integer) 0
```

## Best Practices

- Check if the key exists before using `STRLEN` if you expect a specific behavior based on the existence of the key.
- Use `STRLEN` to validate data size constraints in applications where string length is critical.

## Common Mistakes

- Using `STRLEN` on keys that are not of string type will result in an error. Ensure the key stores a string value.

## FAQs

### What happens if the key does not exist?

If the specified key does not exist, `STRLEN` returns 0.

### Can I use `STRLEN` on keys with non-string values?

No, `STRLEN` can only be used on keys that store string values. Using it on other types will result in an error.
