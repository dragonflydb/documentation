---
description: Learn how to use Redis JSON.DEL command to delete a key from a JSON document.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.DEL

<PageTitle title="Redis JSON.DEL Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.DEL` is a Redis command provided by the RedisJSON module to delete a key or a specific path in a JSON document. It is useful for managing parts of complex JSON objects stored in Redis, allowing you to remove unnecessary or outdated information without affecting other data.

## Syntax

```cli
JSON.DEL <key> [path]
```

## Parameter Explanations

- `key`: The key where the JSON document is stored.
- `path`: (Optional) A JSONPath expression that specifies the part of the JSON document to delete. If omitted, the entire JSON document will be deleted.

## Return Values

- `(integer)`: The number of paths deleted (0 if the key does not exist or the path does not match).

## Code Examples

```cli
dragonfly> JSON.SET mydoc $ '{"name": "John", "age": 30, "city": "New York"}'
OK
dragonfly> JSON.DEL mydoc $..age
(integer) 1
dragonfly> JSON.GET mydoc
"{\"name\":\"John\",\"city\":\"New York\"}"

dragonfly> JSON.SET mydoc $ '{"name": "John", "age": 30, "city": "New York"}'
OK
dragonfly> JSON.DEL mydoc
(integer) 1
dragonfly> JSON.GET mydoc
(nil)
```

## Best Practices

- Always ensure the path exists before attempting to delete it to avoid unexpected behavior.
- Use `JSON.TYPE` to verify the structure of the JSON document if uncertain about the path.

## Common Mistakes

- Providing an incorrect path which results in a zero deletion count.
- Assuming the entire document is deleted when specifying a path; only the specified part is removed.

## FAQs

### Can I use wildcards in the path for `JSON.DEL`?

Yes, you can use JSONPath expressions with wildcards to target multiple elements for deletion.

### What happens if the key does not exist?

The command returns `(integer) 0`, indicating no paths were deleted.
