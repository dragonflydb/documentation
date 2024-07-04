---
description: Learn how to use Redis SETRANGE to overwrite part of a string at the specified key.
---

import PageTitle from '@site/src/components/PageTitle';

# SETRANGE

<PageTitle title="Redis SETRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SETRANGE` command in Redis is used to overwrite part of a string at a specified range. This command is useful for modifying parts of an existing string without replacing the entire value, which can be beneficial when working with large strings or binary data. Typical use cases include updating specific fields within a structured string or modifying sections of a binary blob.

## Syntax

```plaintext
SETRANGE key offset value
```

## Parameter Explanations

- `key`: The name of the key that holds the string value.
- `offset`: The zero-based byte offset where the modification should begin.
- `value`: The string to be inserted starting at the specified offset.

## Return Values

The `SETRANGE` command returns the length of the string after the modification.

Example:

```cli
(integer) 13
```

## Code Examples

```cli
dragonfly> SET mykey "Hello World"
OK
dragonfly> SETRANGE mykey 6 "Redis"
(integer) 11
dragonfly> GET mykey
"Hello Redis"
```

In this example:

1. The initial value of `mykey` is set to "Hello World".
2. The `SETRANGE` command modifies the string starting at offset 6, changing "World" to "Redis".
3. The final string is "Hello Redis".

## Best Practices

- Ensure that the `offset` provided does not cause unintentional padding with null bytes, especially if the string length extends significantly.
- Use `SETRANGE` for modifying existing parts of a string rather than constructing new complex strings from scratch.

## Common Mistakes

- Using `SETRANGE` on non-string keys will result in an error.
- Specifying an `offset` beyond the current string length may lead to unexpected results due to implicit padding with null bytes.

## FAQs

### What happens if the offset is larger than the current string length?

If the `offset` is beyond the current length of the string, Redis pads the string with null bytes up to the specified offset before adding the new value.

### Can I use `SETRANGE` on keys holding types other than strings?

No, `SETRANGE` only works with keys that hold string values. Applying it to a non-string key will result in an error.
