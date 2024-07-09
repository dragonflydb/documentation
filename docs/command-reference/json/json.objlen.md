---
description: Learn using Redis JSON.OBJLEN command to get the length of a JSON object.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.OBJLEN

<PageTitle title="Redis JSON.OBJLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.OBJLEN` command in Redis is used to get the number of keys in a JSON object stored at a specified path. It is part of the RedisJSON module, which allows you to manipulate JSON data directly within Redis. This command is particularly useful for quickly retrieving the size of a JSON object without needing to fetch and parse the entire object.

## Syntax

```plaintext
JSON.OBJLEN <key> [path]
```

## Parameter Explanations

- `<key>`: The key under which the JSON document is stored.
- `[path]`: (Optional) The path to the JSON object whose length is to be retrieved. Defaults to the root if not specified.

## Return Values

The command returns an integer representing the number of keys in the specified JSON object.

### Example Outputs

- If the JSON object has 3 keys, the output will be:
  ```plaintext
  (integer) 3
  ```
- If the specified path does not point to a JSON object, the output will be:
  ```plaintext
  (nil)
  ```

## Code Examples

```cli
dragonfly> JSON.SET myjson $ '{"name":"John","age":30,"city":"New York"}'
OK
dragonfly> JSON.OBJLEN myjson $
(integer) 3
dragonfly> JSON.SET myjson $ '{"person":{"name":"John","age":30},"city":"New York"}'
OK
dragonfly> JSON.OBJLEN myjson $.person
(integer) 2
dragonfly> JSON.OBJLEN myjson $.city
(nil)
```

## Best Practices

- Always ensure that the path provided points to a valid JSON object. Using a path that points to a non-object type (e.g., string, array) will result in a nil response.
- Combine `JSON.OBJLEN` with other JSON commands to efficiently manage and query your JSON data within Redis.

## Common Mistakes

- Providing an incorrect path that does not lead to a JSON object can cause confusion. Double-check paths to ensure they are correct.
- Assuming that the command will work on non-object types like arrays or strings. The `JSON.OBJLEN` command is specifically designed for objects.

## FAQs

### What happens if I provide a non-existent key?

If you provide a key that does not exist, the result will be `(nil)`.

### Can I use JSON.OBJLEN on JSON arrays or strings?

No, `JSON.OBJLEN` is specifically for counting the keys in a JSON object. It will return `(nil)` if used on other types like arrays or strings.
