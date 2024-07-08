---
description: Learn how to use Redis LREM command to remove matching elements from a list.
---

import PageTitle from '@site/src/components/PageTitle';

# LREM

<PageTitle title="Redis LREM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LREM` command in Redis is used to remove elements from a list based on their value. This command is particularly useful for scenarios where you need to clean up or modify a list by removing specific occurrences of a given element.

## Syntax

```plaintext
LREM key count element
```

## Parameter Explanations

- `key`: The name of the list from which to remove elements.
- `count`: An integer that determines how many occurrences of the element to remove:
  - If `count` is positive, it removes elements equal to `element` moving from head to tail.
  - If `count` is negative, it removes elements equal to `element` moving from tail to head.
  - If `count` is zero, all occurrences of `element` are removed.
- `element`: The value to be removed from the list.

## Return Values

The command returns an integer representing the number of removed elements.

## Code Examples

```cli
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> RPUSH mylist "two"
(integer) 4
dragonfly> LREM mylist 1 "two"
(integer) 1
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "three"
3) "two"
dragonfly> LREM mylist 0 "two"
(integer) 1
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "three"
```

## Best Practices

- When using `LREM`, always ensure that the list exists to avoid unnecessary errors.
- Be cautious with the `count` parameter, especially when set to zero, as it will remove all instances of the specified element, which might not always be desirable.

## Common Mistakes

- Using a non-existent key: This results in no action but can lead to confusion if not checked beforehand.
- Incorrect use of the `count` parameter: Misunderstanding its purpose could lead to unexpected deletions from your list.

## FAQs

### How does `LREM` handle non-existent elements?

If the specified element does not exist in the list, `LREM` simply returns `0` indicating no elements were removed.

### Can I use `LREM` on non-list data types?

No, `LREM` is designed to work only with lists. Applying it to other data types will result in an error.
