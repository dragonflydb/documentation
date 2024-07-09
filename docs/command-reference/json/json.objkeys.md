---
description: Discover Redis JSON.OBJKEYS command to fetch keys from a JSON object.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.OBJKEYS

<PageTitle title="Redis JSON.OBJKEYS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `JSON.OBJKEYS` command is used to retrieve the keys of a JSON object stored in Redis. This command is part of the RedisJSON module, which allows for manipulation and querying of JSON documents stored as Redis keys. Typical use cases include examining the structure of a JSON object, validating the existence of specific keys, and iterating over the key names for further processing.

## Syntax

```plaintext
JSON.OBJKEYS <key> [path]
```

## Parameter Explanations

- `<key>`: The Redis key where the JSON object is stored.
- `[path]`: An optional JSONPath expression to specify the location within the JSON document. If omitted, defaults to the root (`$`).

## Return Values

- **Array**: Returns an array of strings representing the keys at the provided JSON path.
- **Null**: Returns `null` if the path does not exist or is not a valid JSON object path.

### Example Output

```plaintext
1) "name"
2) "age"
3) "address"
```

## Code Examples

```cli
dragonfly> JSON.SET mydoc $ '{"name":"John", "age":30, "address":{"city":"New York","zip":"10001"}}'
OK
dragonfly> JSON.OBJKEYS mydoc $
1) "name"
2) "age"
3) "address"
dragonfly> JSON.OBJKEYS mydoc $.address
1) "city"
2) "zip"
```

## Best Practices

- Ensure that the paths provided are accurate to avoid unexpected null returns.
- Use JSON.OBJKEYS to validate the structure of your JSON objects before performing operations that depend on specific keys.

## Common Mistakes

- **Invalid Path**: Providing an incorrect JSONPath, resulting in a null return.
- **Non-Object Paths**: Using JSON.OBJKEYS on a path that does not resolve to a JSON object; it only works with objects, not arrays or primitive values.

## FAQs

### What happens if I provide a path that does not exist?

If the specified path does not exist or does not lead to a JSON object, the command will return `null`.

### Can I use JSON.OBJKEYS on arrays?

No, `JSON.OBJKEYS` is specifically designed for JSON objects. Using it on arrays will result in a null return.
