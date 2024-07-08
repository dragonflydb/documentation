---
description: Learn how to use Redis LPUSH command to insert an element at the start of a list.
---

import PageTitle from '@site/src/components/PageTitle';

# LPUSH

<PageTitle title="Redis LPUSH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LPUSH` command in Redis is used to insert one or more elements at the head of a list. This can be useful for queue implementations, task scheduling, or simply maintaining a list where new entries should appear first.

## Syntax

```plaintext
LPUSH key element [element ...]
```

## Parameter Explanations

- **key**: The name of the list.
- **element**: One or more elements to insert at the head of the list.

## Return Values

`LPUSH` returns an integer representing the length of the list after the push operation.

Example:

```plaintext
(integer) 3
```

## Code Examples

```cli
dragonfly> LPUSH mylist "world"
(integer) 1
dragonfly> LPUSH mylist "hello"
(integer) 2
dragonfly> LPUSH mylist "!"
(integer) 3
dragonfly> LRANGE mylist 0 -1
1) "!"
2) "hello"
3) "world"
```

## Best Practices

- Pre-check if the list exists to avoid unintended behavior when working with non-list data types.
- Use `LPUSH` in combination with `LTRIM` to maintain a fixed list size, helpful for queue management.

## Common Mistakes

- **Incorrect Data Type**: Using `LPUSH` on a key that holds a non-list value will result in an error. Always ensure the key corresponds to a list.
- **Order Confusion**: Remember that `LPUSH` adds elements to the head (left end), not the tail (right end) of the list.

## FAQs

### What happens if the list does not exist?

If the list does not exist, `LPUSH` creates it before inserting elements.

### Can I insert multiple elements at once?

Yes, you can specify multiple elements, and they will be inserted in the same order as provided from left to right.

### How can I ensure that the list does not grow indefinitely?

Use `LTRIM` in combination with `LPUSH` to keep the list length within a certain limit.

```cli
dragonfly> LPUSH mylist "new_element"
(integer) 4
dragonfly> LTRIM mylist 0 2
OK
```
