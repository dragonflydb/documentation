---
description: Learn how to use Redis JSON.ARRINDEX command to find the index of an element in a JSON array.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRINDEX

<PageTitle title="Redis JSON.ARRINDEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.ARRINDEX` is a command in Redis used with the ReJSON module to find the index of a specified element within a JSON array. This command is particularly useful when working with JSON data structures stored in Redis and you need to locate an element's position within an array. Typical scenarios include checking for the existence of elements, retrieving specific data points, and manipulating arrays based on their contents.

## Syntax

```plaintext
JSON.ARRINDEX <key> <path> <json-scalar> [start [stop]]
```

## Parameter Explanations

- **`<key>`**: The key under which the JSON data is stored.
- **`<path>`**: The path in the JSON document where the array resides.
- **`<json-scalar>`**: The scalar value (string, number, or boolean) to search for within the array.
- **`[start]`**: Optional parameter specifying the starting index to begin the search from. Default is 0.
- **`[stop]`**: Optional parameter specifying the stopping index to end the search. Default is the end of the array.

## Return Values

The command returns the index of the first occurrence of the specified element within the array. If the element is not found, it returns `-1`.

Examples:

```plaintext
(integer) 2
(integer) -1
```

## Code Examples

```cli
dragonfly> JSON.SET mydoc $ '{"numbers": [1, 2, 3, 4, 5]}'
OK
dragonfly> JSON.ARRINDEX mydoc $.numbers 3
(integer) 2
dragonfly> JSON.ARRINDEX mydoc $.numbers 6
(integer) -1
dragonfly> JSON.ARRINDEX mydoc $.numbers 4 1 3
(integer) 3
```

## Best Practices

- Ensure that the path specified is correct and points to a JSON array; otherwise, the command will not work as intended.
- Use the optional `start` and `stop` parameters to narrow the search range, especially for large arrays, to improve performance.

## Common Mistakes

- Using incorrect paths can lead to unexpected results or errors.
- Forgetting to specify the `start` and `stop` parameters when needed can cause the command to search the entire array, potentially leading to inefficiencies.

## FAQs

### What happens if the JSON path does not point to an array?

If the specified path does not point to an array, the command will return an error indicating that the path is invalid for this operation.

### Can I use JSON.ARRINDEX to search for nested objects within an array?

No, `JSON.ARRINDEX` only works with scalar values (strings, numbers, booleans). For more complex searches, consider other commands or restructuring your JSON data.
