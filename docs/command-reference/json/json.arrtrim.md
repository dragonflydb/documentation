---
description: Get to know about the Redis JSON.ARRTRIM command to trim an array to a specified range.
---

import PageTitle from '@site/src/components/PageTitle';

# JSON.ARRTRIM

<PageTitle title="Redis JSON.ARRTRIM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`JSON.ARRTRIM` is a command in Redis used to trim an array in a JSON document stored at a specified key. This command is particularly useful when you need to keep only a specific range of elements within an array, effectively removing all other elements outside this range. Typical scenarios include maintaining a fixed-size recent log of events or limiting the number of items in a user's shopping cart.

## Syntax

```plaintext
JSON.ARRTRIM <key> <path> <start> <stop>
```

## Parameter Explanations

- **key**: The key of the JSON document in which you want to trim the array.
- **path**: The JSON path pointing to the array you wish to trim.
- **start**: The starting index of the array range you want to retain (inclusive).
- **stop**: The ending index of the array range you want to retain (inclusive).

## Return Values

The command returns the length of the array after the trim operation.

### Example Outputs

- If the array is successfully trimmed:
  ```plaintext
  (integer) 3
  ```
- If the specified path does not exist:
  ```plaintext
  (integer) 0
  ```

## Code Examples

```cli
dragonfly> JSON.SET mydoc $ '{"items": [1, 2, 3, 4, 5]}'
OK
dragonfly> JSON.ARRTRIM mydoc $.items 1 3
(integer) 3
dragonfly> JSON.GET mydoc $
"{\"items\":[2,3,4]}"
dragonfly> JSON.ARRTRIM mydoc $.items 0 1
(integer) 2
dragonfly> JSON.GET mydoc $
"{\"items\":[2,3]}"
```

## Best Practices

When using `JSON.ARRTRIM`, ensure that the specified start and stop indices are within the bounds of the array to avoid unexpected results. Always validate the existence of the array at the given JSON path before performing trim operations.

## Common Mistakes

- **Incorrect Path**: Specifying a non-existent or incorrect path will result in no operation being performed.
- **Out-of-Bounds Indices**: Using start or stop indices outside the valid range of the array can lead to unexpected behavior or errors.
- **Negative Indices**: Redis does not support negative indices for this command; ensure that indices are non-negative.

## FAQs

### What happens if the start or stop indices are out of range?

If the start or stop indices are out of the array's range, Redis will adjust them to fit within the valid range, potentially resulting in an empty array.

### Can I use negative indices with JSON.ARRTRIM?

No, Redis does not support negative indices for the `JSON.ARRTRIM` command. Use only non-negative integers.
