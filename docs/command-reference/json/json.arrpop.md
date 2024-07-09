---
description: Understand how to use Redis JSON.ARRPOP command to remove and return the last element of an array.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRPOP

<PageTitle title="Redis JSON.ARRPOP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.ARRPOP` is a RedisJSON command used to remove and return an element from the specified index of a JSON array stored in a key. This command is useful for modifying JSON arrays stored in Redis without retrieving and re-storing the entire value, making it efficient for operations where you need to manipulate arrays directly.

## Syntax

```plaintext
JSON.ARRPOP key [path [index]]
```

## Parameter Explanations

- `key`: The key under which the JSON document is stored.
- `path` (optional): The JSON path within the document. Defaults to the root if not provided.
- `index` (optional): The position of the element to pop from the array. A negative index counts from the end of the array. Defaults to -1 (the last element) if not provided.

## Return Values

The command returns the popped element from the JSON array. If the specified path or index does not exist, it will return `null`.

### Example Outputs:

- Popping the last element: `"dragonfly> JSON.ARRPOP myJson $.arrayPath"` -> `10`
- Popping a specific element: `"dragonfly> JSON.ARRPOP myJson $.arrayPath 2"` -> `"three"`

## Code Examples

```cli
dragonfly> JSON.SET myJson $ '{"arrayPath": [1, 2, 3, 4]}'
OK
dragonfly> JSON.ARRPOP myJson $.arrayPath
(integer) 4
dragonfly> JSON.GET myJson
"{\"arrayPath\":[1,2,3]}"
dragonfly> JSON.ARRPOP myJson $.arrayPath 0
(integer) 1
dragonfly> JSON.GET myJson
"{\"arrayPath\":[2,3]}"
```

## Best Practices

- Ensure that the `path` specified points to an array; otherwise, the command will not perform as expected.
- Regularly validate the structure of your JSON data to avoid errors during runtime.

## Common Mistakes

- **Incorrect Path**: Specifying a path that does not point to an array will result in no action taken.
- **Out of Range Index**: Providing an index that exceeds the array's bounds returns `null` without altering the array.

## FAQs

### Can I use `JSON.ARRPOP` on a nested JSON array?

Yes, by specifying the correct path, you can pop elements from nested JSON arrays.

### What happens if the array is empty?

If the array is empty, `JSON.ARRPOP` will return `null`.
