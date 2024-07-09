---
description: Discover how to use Redis JSON.ARRINSERT command to insert an element at a specified position in an array.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRINSERT

<PageTitle title="Redis JSON.ARRINSERT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.ARRINSERT` is a command in Redis used for inserting elements into a JSON array at a specified index. It is particularly useful when you need to dynamically modify JSON data stored in Redis, allowing for the painless insertion of new elements without rewriting the entire array.

## Syntax

```
JSON.ARRINSERT <key> <path> <index> <json>
```

## Parameter Explanations

- `<key>`: The key under which the JSON document is stored.
- `<path>`: The path in the JSON document where the array resides.
- `<index>`: The index at which to insert the new element. If the index is negative, it counts from the end of the array.
- `<json>`: The JSON element to insert into the array.

## Return Values

The command returns the length of the array after the insertion.

```cli
(integer) 4
```

If the path does not exist or is not an array, the command will return `(integer) -1`.

## Code Examples

```cli
dragonfly> JSON.SET myjson . '{"name": "Alice", "hobbies": ["reading", "swimming"]}'
OK

dragonfly> JSON.ARRINSERT myjson $.hobbies 1 '"coding"'
(integer) 3

dragonfly> JSON.GET myjson
{"name":"Alice","hobbies":["reading","coding","swimming"]}
```

Here, the `"coding"` hobby is inserted at index `1` in the `hobbies` array.

## Best Practices

- Always ensure that the path provided points to an array within the JSON document.
- Validate the JSON structure before performing operations to avoid unexpected results.

## Common Mistakes

- Specifying a non-array path: The command will fail if the path does not point to an array.
- Incorrect JSON format: Ensure the JSON string provided as the element is correctly formatted.

## FAQs

### What happens if I use a negative index?

A negative index counts from the end of the array, with `-1` being the last element.

### Can I insert multiple elements at once?

No, `JSON.ARRINSERT` inserts only one element at a time. To insert multiple elements, you need to call the command multiple times.
