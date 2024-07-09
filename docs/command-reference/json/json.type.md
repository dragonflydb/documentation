---
description: Grasp how to use Redis JSON.TYPE command to get the type of data present in a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.TYPE

<PageTitle title="Redis JSON.TYPE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.TYPE` command in Redis is part of the ReJSON module, which allows manipulation and querying of JSON values in Redis. This command returns the type of a specified key or path within a JSON document. Typical use cases include validation of data structures before performing operations on them and debugging to ensure correct data types.

## Syntax

```plaintext
JSON.TYPE <key> [path]
```

## Parameter Explanations

- **key**: The key that holds the JSON document.
- **path**: (Optional) A JSONPath expression specifying the location within the JSON document. If not provided, defaults to the root (`$`).

## Return Values

The command returns the type of the value at the specified path as a string. Possible return types are:

- `"null"`
- `"boolean"`
- `"number"`
- `"string"`
- `"object"`
- `"array"`

Example outputs:

- `"string"` if the value at the specified path is a string.
- `"array"` if the value is an array.
- `nil` if the path does not exist.

## Code Examples

```cli
dragonfly> JSON.SET myjson $ '{"name": "John", "age": 30, "isActive": true}'
OK
dragonfly> JSON.TYPE myjson $
"object"
dragonfly> JSON.TYPE myjson $.name
"string"
dragonfly> JSON.TYPE myjson $.age
"number"
dragonfly> JSON.TYPE myjson $.isActive
"boolean"
dragonfly> JSON.TYPE myjson $.nonexistent
(nil)
```

## Best Practices

- Validate the presence and type of JSON elements before performing operations to avoid errors.
- Use precise JSONPath expressions to target specific elements within complex JSON documents.

## Common Mistakes

- Omitting the path when the intent is to check a nested element, leading to unexpected results.
- Misunderstanding JSONPath syntax, which may result in errors or incorrect path targeting.

## FAQs

### Does `JSON.TYPE` support all JSON data types?

Yes, it supports `null`, `boolean`, `number`, `string`, `object`, and `array`.

### What happens if the path does not exist?

If the specified path does not exist, the command returns `nil`.
