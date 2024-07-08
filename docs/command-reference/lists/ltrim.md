---
description: Learn using Redis LTRIM to precisely control the size of your lists by trimming elements.
---

import PageTitle from '@site/src/components/PageTitle';

# LTRIM

<PageTitle title="Redis LTRIM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`LTRIM` is a Redis command used to trim a list to the specified range of elements. This command is essential for managing the size of lists, especially in scenarios where lists grow dynamically, such as logging systems or task queues, ensuring that memory usage remains within bounds.

## Syntax

```plaintext
LTRIM key start stop
```

## Parameter Explanations

- `key`: The name of the list you want to trim.
- `start`: The starting index of the range (0-based). Negative values indicate offsets from the end of the list (-1 being the last element).
- `stop`: The ending index of the range (inclusive). Negative values are processed similarly to the `start` parameter.

## Return Values

`LTRIM` returns a simple string reply:

- "OK" if the trimming operation was successful.

Example outputs:

```plaintext
OK
```

## Code Examples

```cli
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> RPUSH mylist "four"
(integer) 4
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
3) "three"
4) "four"
dragonfly> LTRIM mylist 1 2
OK
dragonfly> LRANGE mylist 0 -1
1) "two"
2) "three"
```

## Best Practices

- Use `LTRIM` in conjunction with other list operations to manage list sizes efficiently, particularly in applications where lists are used for logs or queues.
- Regularly trim large lists to prevent excessive memory usage.

## Common Mistakes

- Using indices out of the actual list's range will not cause an error but may lead to unexpected results where the list becomes empty.

## FAQs

### What happens if the `start` and `stop` indices are out of bounds?

If the `start` or `stop` indices are outside the actual list's range, Redis will handle it gracefully by trimming the list to an empty state if necessary or adjusting the indices to fit the existing list's boundaries.

### Is `LTRIM` a blocking command?

No, `LTRIM` is not a blocking command and will perform the operation quickly, making it suitable for use in real-time applications.
