---
description: Understand using Redis LPOS for finding the index of a value in a list.
---

import PageTitle from '@site/src/components/PageTitle';

# LPOS

<PageTitle title="Redis LPOS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LPOS` command in Redis is used to find the first occurrence of a specified element in a list. This command is particularly useful when you need to locate an item within a large list without iterating through it manually. Typical scenarios include finding the position of a specific item for further operations or checks.

## Syntax

```
LPOS key element [RANK rank] [COUNT num-matches] [MAXLEN len]
```

## Parameter Explanations

- **key**: The name of the list.
- **element**: The value to search for within the list.
- **RANK rank**: Optional. Specifies which occurrence of the element you are looking for (1-based index). By default, it is 1.
- **COUNT num-matches**: Optional. The number of matches to return. Default is 1.
- **MAXLEN len**: Optional. Limits the search to the first `len` elements of the list.

## Return Values

The `LPOS` command returns:

- An integer if only one match is requested (default behavior).
- An array of integers if multiple matches are requested using the `COUNT` option.
- `nil` if the element is not found.

### Examples:

- Single match (default): `3`
- Multiple matches: `[3, 7, 10]`
- Not found: `(nil)`

## Code Examples

```cli
dragonfly> RPUSH mylist "a" "b" "c" "d" "b" "e"
(integer) 6
dragonfly> LPOS mylist "b"
(integer) 1
dragonfly> LPOS mylist "b" RANK 2
(integer) 4
dragonfly> LPOS mylist "b" COUNT 2
1) (integer) 1
2) (integer) 4
dragonfly> LPOS mylist "b" MAXLEN 3
(integer) 1
```

## Best Practices

- Use the `MAXLEN` option to limit search scope in very large lists to improve performance.
- When expecting multiple occurrences, use the `COUNT` option to get all necessary positions in one go.

## Common Mistakes

- Forgetting that the `RANK` parameter is 1-based, which can lead to off-by-one errors.
- Not specifying `COUNT` when expecting multiple results, leading to only the first occurrence being returned.

## FAQs

### How do I find the second occurrence of an element in a list?

Use the `RANK` parameter set to 2:

```cli
dragonfly> LPOS mylist "b" RANK 2
```

### What happens if the element is not found?

The command returns `nil`.
