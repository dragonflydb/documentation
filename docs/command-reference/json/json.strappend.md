---
description: Discover the Redis JSON.STRAPPEND command for appending strings in a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.STRAPPEND

<PageTitle title="Redis JSON.STRAPPEND Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.STRAPPEND` command in Redis is used to append a string value to an existing string stored within a JSON document. This is particularly useful for modifying JSON structures without the need to retrieve, modify, and set the entire document, thereby improving performance and reducing complexity.

Typical scenarios include updating logs, concatenating strings, or gradually building up a string value within a JSON object.

## Syntax

```plaintext
JSON.STRAPPEND <key> <path> <json-string>
```

## Parameter Explanations

- **`<key>`**: The key under which the JSON document is stored.
- **`<path>`**: The JSON path to the string value that you want to append to. This follows the JSONPath syntax.
- **`<json-string>`**: The string value to be appended to the existing string at the specified path. It must be a valid JSON string.

## Return Values

The command returns the length of the new string after the append operation.

### Examples of possible outputs:

- If the original string was `"foo"` and you append `"bar"`, the return value will be the length of `"foobar"`, which is `6`.
- An error if the path does not exist or the value at the path is not a string.

## Code Examples

```cli
dragonfly> JSON.SET mydoc . '{"greeting": "Hello"}'
OK
dragonfly> JSON.STRAPPEND mydoc .greeting '" World!"'
(integer) 12
dragonfly> JSON.GET mydoc .greeting
"Hello World!"
```

## Best Practices

- Ensure that the path points to a string value; otherwise, the command will result in an error.
- Always validate the JSON structure before performing operations to avoid unexpected behaviors.

## Common Mistakes

- **Appending to Non-String Values**: Attempting to append to a non-string type will cause an error. Ensure the target path holds a string.
- **Incorrect JSON Path**: Using an incorrect path format can lead to command failure. Double-check the JSONPath syntax.

## FAQs

### What happens if the path does not exist?

If the specified path does not exist or points to a non-string value, the command will result in an error.

### Can I append multiple strings in one command?

No, `JSON.STRAPPEND` only allows appending a single string at a time. For multiple appends, multiple commands are required.
