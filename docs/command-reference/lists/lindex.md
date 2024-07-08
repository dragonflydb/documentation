---
description: Learn to use Redis LINDEX to retrieve an element from a specified position in a list.
---

import PageTitle from '@site/src/components/PageTitle';

# LINDEX

<PageTitle title="Redis LINDEX Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`LINDEX` is a Redis command used to retrieve an element from a list by its index. This is especially useful in scenarios where you need to access specific elements within lists stored in Redis, such as retrieving user information or configuration settings at a particular position.

## Syntax

```plaintext
LINDEX key index
```

## Parameter Explanations

- `key`: The name of the list from which to retrieve the element.
- `index`: The zero-based position in the list of the desired element. Negative indices can be used to count from the end of the list, with `-1` being the last element, `-2` being the second-last, and so on.

## Return Values

The command returns the element at the specified index in the list. If the index is out of range, it returns `nil`.

### Examples:

- An existing element: `"element"`
- Out of range: `(nil)`

## Code Examples

```cli
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> LINDEX mylist 0
"one"
dragonfly> LINDEX mylist 1
"two"
dragonfly> LINDEX mylist -1
"three"
dragonfly> LINDEX mylist 5
(nil)
```

## Best Practices

- Ensure the list exists and contains sufficient elements before using `LINDEX` to avoid unexpected `nil` results.
- Use negative indexing to simplify retrieval of items from the end of the list without knowing the exact length.

## Common Mistakes

- Using an invalid key type: `LINDEX` should only be used with Redis lists. Using it with other data types like strings or sets will result in errors.
- Misinterpreting negative indices: Negative indices are relative to the end of the list, not absolute positions from the start.

## FAQs

### What happens if the index is out of range?

If the specified index is out of the range of the list, `LINDEX` returns `nil`.

### Can I use `LINDEX` with non-list data types?

No, `LINDEX` is specific to lists in Redis. Using it with other data types (strings, sets, hashes, etc.) will cause an error.
