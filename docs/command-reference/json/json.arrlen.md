---
description: Learn how to use Redis JSON.ARRLEN command to find the length of a JSON array.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRLEN

<PageTitle title="Redis JSON.ARRLEN Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.ARRLEN` is a command provided by Redis modules like RedisJSON, used to get the length of a JSON array at a specific path in a JSON document. This is particularly useful when working with data structures that require frequent inspection or processing of JSON arrays within Redis.

## Syntax

```plaintext
JSON.ARRLEN <key> [path]
```

## Parameter Explanations

- **`key`**: The key under which the JSON document is stored.
- **`path`**: (Optional) The JSONPath to the array within the JSON document. If no path is provided, the root path (`"."`) is assumed.

## Return Values

Returns the length of the JSON array at the specified path. If the path does not exist or if it doesn't point to an array, the command will return `null`.

Example outputs:

- If the array length is 3: `(integer) 3`
- If the path does not exist: `null`

## Code Examples

```cli
dragonfly> JSON.SET mydoc . '{"numbers": [1, 2, 3]}'
OK
dragonfly> JSON.ARRLEN mydoc .numbers
(integer) 3
dragonfly> JSON.SET mydoc . '{"nested": {"array": [10, 20]}}'
OK
dragonfly> JSON.ARRLEN mydoc .nested.array
(integer) 2
dragonfly> JSON.ARRLEN mydoc .nonexistent.path
(nil)
```

## Best Practices

When using `JSON.ARRLEN`, ensure that the path provided accurately refers to an array. Misidentifying the path can lead to unexpected `null` results.

## Common Mistakes

- **Incorrect Path**: Providing an incorrect or non-existent path will result in `null`.
- **Non-array Data Type**: Attempting to use `JSON.ARRLEN` on a path that doesn't contain an array will also result in `null`.

## FAQs

### What happens if the path points to a non-array element?

The command will return `null`.

### Can I use JSON.ARRLEN on multiple paths in one command?

No, `JSON.ARRLEN` operates on a single path per command. You need to issue separate commands for each path.
