---
description: Learn how to use the Redis JSON.RESP command to change the response format of JSON commands.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.RESP

<PageTitle title="Redis JSON.RESP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.RESP` is a command provided by Redis for converting a JSON document into RESP (Redis Serialization Protocol) format, making it easier to manipulate and work with JSON data directly within Redis. This command is typically used when you need to interface JSON data with Redis commands or when you want to inspect and debug JSON structures in a more readable format.

## Syntax

```cli
JSON.RESP <key> [path]
```

## Parameter Explanations

- **`key`**: The key where the JSON document is stored.
- **`path`**: (Optional) The path within the JSON document to convert into RESP format. If omitted, the entire JSON document is converted.

## Return Values

The command returns the JSON structure in RESP format. Here are some examples:

1. For a JSON object:

   ```json
   { "name": "John", "age": 30 }
   ```

   RESP format output:

   ```cli
   1) "name"
   2) "John"
   3) "age"
   4) (integer) 30
   ```

2. For a JSON array:
   ```json
   ["apple", "banana", "cherry"]
   ```
   RESP format output:
   ```cli
   1) "apple"
   2) "banana"
   3) "cherry"
   ```

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"name": "John", "age": 30, "hobbies": ["reading", "swimming"]}'
OK
dragonfly> JSON.RESP myjson .
1) "name"
2) "John"
3) "age"
4) (integer) 30
5) "hobbies"
6) 1) "reading"
   2) "swimming"

dragonfly> JSON.RESP myjson .name
1) "John"

dragonfly> JSON.RESP myjson .hobbies
1) "reading"
2) "swimming"
```

## Best Practices

- When working with large JSON documents, use specific paths to avoid unnecessary processing of the entire document.
- Ensure that the JSON data is properly formatted before using `JSON.RESP` to prevent errors.

## Common Mistakes

- Omitting the key parameter will result in a syntax error.
- Providing an incorrect path might return unexpected results or nil values.

## FAQs

### What happens if the specified path does not exist?

If the specified path within the JSON document does not exist, the command will return a null response.

### Can I use JSON.RESP with nested JSON objects?

Yes, you can specify paths to access nested JSON objects and convert them into RESP format.
