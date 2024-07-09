---
description: Understand how to use Redis JSON.ARRAPPEND command to append an element into a JSON array.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRAPPEND

<PageTitle title="Redis JSON.ARRAPPEND Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.ARRAPPEND` is used in Redis to append elements to a JSON array stored at a specified key. It is particularly useful in scenarios where you need to dynamically grow a JSON array with new data elements, such as logging events, aggregating data, or maintaining ordered lists within a JSON document.

## Syntax

```cli
JSON.ARRAPPEND <key> <path> <element> [<element> ...]
```

## Parameter Explanations

- **key**: The key of the JSON document.
- **path**: The JSON path to the array within the document where elements will be appended. Typically starts with `.`.
- **element**: One or more elements to append to the array. These can be any valid JSON types (e.g., strings, numbers, objects).

## Return Values

Returns an integer representing the new length of the array after the elements have been appended.

### Example Outputs:

- `(integer) 2`: Indicates that two elements are now in the array.
- `(integer) 5`: Indicates that five elements are now in the array.

## Code Examples

```cli
dragonfly> JSON.SET mydoc . '{"numbers":[1, 2, 3]}'
OK
dragonfly> JSON.ARRAPPEND mydoc .numbers 4
(integer) 4
dragonfly> JSON.ARRAPPEND mydoc .numbers 5 6
(integer) 6
dragonfly> JSON.GET mydoc
"{\"numbers\":[1,2,3,4,5,6]}"
```

## Best Practices

- Ensure that the path points to a valid JSON array; otherwise, an error will occur.
- Consider using indexed paths to manage large arrays efficiently.

## Common Mistakes

- Appending to a non-array path will result in an error.
- Providing invalid JSON elements can cause command failure.

## FAQs

### What happens if the path does not exist?

If the specified path does not exist and cannot be created, the command will return an error.

### Can I append multiple elements at once?

Yes, you can append multiple elements by listing them after the path parameter.
