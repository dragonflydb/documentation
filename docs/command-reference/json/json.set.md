---
description: Find how to use Redis JSON.SET command to set a JSON document in a database.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.SET

<PageTitle title="Redis JSON.SET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.SET` is a command in Redis used with the RedisJSON module for setting JSON values at a specified key. It allows you to store, update, and manipulate JSON data structures in Redis. Common use cases involve storing complex data structures like user profiles, configuration settings, or any other hierarchical data that benefits from being stored as JSON.

## Syntax

```plaintext
JSON.SET <key> <path> <json>
```

## Parameter Explanations

- `<key>`: The key under which the JSON value is stored. This should be a string.
- `<path>`: A JSONPath expression indicating where in the JSON structure the value should be set. Use `$` to refer to the root.
- `<json>`: The JSON data to set at the specified path. This can be any valid JSON value (object, array, number, string, `true`, `false`, or `null`).

## Return Values

The `JSON.SET` command returns `OK` if the operation was successful. If there is an error, such as invalid JSON syntax or an invalid path, an error message is returned.

## Code Examples

```cli
dragonfly> JSON.SET user1 $ '{"name": "Alice", "age": 30}'
"OK"
dragonfly> JSON.SET user1 $.address '{"city": "Wonderland"}'
"OK"
dragonfly> JSON.SET user1 $.age 31
"OK"
dragonfly> JSON.GET user1 $
"{\"name\":\"Alice\",\"age\":31,\"address\":{\"city\":\"Wonderland\"}}"
```

## Best Practices

- Always ensure that the JSON data is well-formed before setting it in Redis to avoid syntax errors.
- Use specific paths to update parts of a JSON document without overwriting the entire structure, which can help maintain data integrity and reduce bandwidth usage.

## Common Mistakes

- Using incorrect JSONPath expressions can lead to errors or unexpected behavior. Verify your JSONPath before using it with `JSON.SET`.
- Overwriting JSON data unintentionally by not specifying the correct path.

## FAQs

### What happens if I set a JSON value at a non-existent key?

If the specified key does not exist, `JSON.SET` will create it and store the provided JSON data.

### Can I use JSON.SET to update nested fields?

Yes, you can specify a path to a nested field to update only that part of the JSON document.

### Does JSON.SET validate the JSON data before storing it?

Yes, `JSON.SET` performs validation to ensure that the JSON data is well-formed. If the data is invalid, an error message will be returned.
