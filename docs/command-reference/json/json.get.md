---
description: Learn using Redis JSON.GET command to retrieve a value from a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.GET

<PageTitle title="Redis JSON.GET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.GET` is a command in Redis used to retrieve JSON values stored at a specific key. This command is especially useful in scenarios where you need to work with JSON data structures, enabling efficient storage and retrieval of complex data.

## Syntax

```
JSON.GET <key> [path]
```

## Parameter Explanations

- `<key>`: The key under which the JSON value is stored.
- `[path]`: (Optional) A JSONPath expression to specify which part of the JSON data should be retrieved. Defaults to the root if not provided.

## Return Values

The command returns the JSON value stored at the specified key or path. If the key does not exist, it returns `nil`.

Examples:

- Full JSON object: `{"name":"John", "age":30}`
- Specific field: `"John"`

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"name": "John", "age": 30}'
OK
dragonfly> JSON.GET myjson
"{\"name\":\"John\",\"age\":30}"
dragonfly> JSON.GET myjson $.name
"\"John\""
```

## Best Practices

- Use paths to retrieve only the necessary parts of your JSON document, improving performance and reducing bandwidth usage.
- Ensure correct JSONPath syntax to avoid unexpected results.

## Common Mistakes

- Forgetting to include the path parameter when needed can result in retrieving the entire JSON object instead of a specific part.
- Using incorrect JSONPath syntax can lead to errors or unexpected outputs.

## FAQs

### What happens if the key does not exist?

If the specified key does not exist, `JSON.GET` will return `nil`.

### Can I use JSON.GET with nested JSON objects?

Yes, you can use JSONPath syntax to target specific fields within nested JSON objects.
