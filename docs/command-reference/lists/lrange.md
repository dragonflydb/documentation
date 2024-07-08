---
description: Understand how to use Redis LRANGE to fetch a range of elements from a list.
---

import PageTitle from '@site/src/components/PageTitle';

# LRANGE

<PageTitle title="Redis LRANGE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LRANGE` command in Redis is used to return a specified range of elements from a list. This command is particularly useful when you need to retrieve a subset of list elements, such as the most recent items in a log or a specific page of results in a paginated dataset.

## Syntax

```plaintext
LRANGE key start stop
```

## Parameter Explanations

- **key**: The name of the list from which to retrieve elements.
- **start**: The starting index of the range (0-based). Negative values can be used to specify offsets from the end of the list; for example, -1 represents the last element.
- **stop**: The ending index of the range (inclusive). Negative values can also be used here.

## Return Values

The `LRANGE` command returns a list of elements within the specified range. If the `start` or `stop` indices are out of bounds, it will simply return an empty list or the truncated part of the list that exists within the bounds.

### Example Outputs

- If the list contains the elements ["a", "b", "c", "d", "e"]:

  ```cli
  dragonfly> LRANGE mylist 0 2
  1) "a"
  2) "b"
  3) "c"
  ```

- If `start` is greater than the length of the list, an empty list is returned:
  ```cli
  dragonfly> LRANGE mylist 10 20
  (empty list)
  ```

## Code Examples

```cli
dragonfly> RPUSH mylist "a" "b" "c" "d" "e"
(integer) 5
dragonfly> LRANGE mylist 0 2
1) "a"
2) "b"
3) "c"
dragonfly> LRANGE mylist -3 -1
1) "c"
2) "d"
3) "e"
dragonfly> LRANGE mylist 1 -2
1) "b"
2) "c"
3) "d"
dragonfly> LRANGE mylist 10 20
(empty list)
```

## Best Practices

- Use negative indices to easily access elements from the end of the list without needing to know its exact length.
- Be mindful of list size and the impact on performance when accessing large ranges. Consider breaking down large lists or using pagination techniques with appropriate `start` and `stop` indices.

## Common Mistakes

- Confusing the `start` and `stop` parameters can lead to unexpected results. Always ensure `start` comes before `stop` logically.
- Using non-existent keys will result in an empty list rather than an error, which might hide issues in your code logic.

## FAQs

### What happens if the list is empty?

If the list is empty, the `LRANGE` command will return an empty list.

### Can I use `LRANGE` with non-list data types?

No, `LRANGE` is specific to lists. Using it with other data types will result in an error.

### How does `LRANGE` handle out-of-bound indices?

Out-of-bound indices do not cause an error; instead, they return the existing portion of the list within those bounds or an empty list if completely outside any valid range.
