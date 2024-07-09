---
description: Discover using Redis JSON.MGET command to retrieve multiple JSON documents from a database.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.MGET

<PageTitle title="Redis JSON.MGET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.MGET` is a command in Redis that retrieves the values at specified paths from multiple JSON keys. It is used when you need to extract specific parts of JSON documents stored under various keys in Redis. This command is essential for applications requiring efficient bulk retrieval of JSON data.

## Syntax

```
JSON.MGET key [key ...] path
```

## Parameter Explanations

- `key [key ...]`: One or more keys from which to retrieve JSON values.
- `path`: A JSONPath expression indicating the part of the JSON documents to fetch.

## Return Values

The command returns an array containing the values at the specified path for each provided key. If a key does not exist, it returns `null` for that key's position in the array.

Example:

- Keys exist: `[value1, value2, value3]`
- Some keys do not exist: `[value1, null, value3]`

## Code Examples

```cli
dragonfly> JSON.SET doc1 $ '{"name":"John", "age":30}'
OK
dragonfly> JSON.SET doc2 $ '{"name":"Jane", "age":25}'
OK
dragonfly> JSON.MGET doc1 doc2 $.name
1) "John"
2) "Jane"
dragonfly> JSON.MGET doc1 doc2 doc3 $.age
1) 30
2) 25
3) (nil)
```

## Best Practices

- Ensure paths are correctly specified using JSONPath syntax to avoid unexpected results.
- Validate the existence of keys before performing operations that depend on their presence to manage nil values gracefully.

## Common Mistakes

- Using incorrect JSONPath expressions can lead to undesired outputs. Always test your paths with known data structures first.
- Requesting paths from empty or non-existent keys will return `null`, which might need handling in application logic.

## FAQs

### Can I use `JSON.MGET` with non-JSON keys?

No, `JSON.MGET` works only with keys containing JSON documents. Using it with non-JSON keys will result in an error.

### What happens if one of the keys does not exist?

If one of the keys does not exist, `JSON.MGET` will return `null` for that key's position in the resulting array.
