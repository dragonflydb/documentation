---
description: Learn how to use the Redis LINSERT command to insert an element before or after a pivot in the list.
---

import PageTitle from '@site/src/components/PageTitle';

# LINSERT

<PageTitle title="Redis LINSERT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LINSERT` command in Redis is used to insert an element before or after another element in a list. This command is particularly useful when you need to maintain a specific order in a list and want to add elements dynamically without having to retrieve and rewrite the entire list.

## Syntax

```plaintext
LINSERT key BEFORE|AFTER pivot element
```

## Parameter Explanations

- **key**: The name of the list where the insertion will happen.
- **BEFORE|AFTER**: Specifies whether the new element should be inserted before or after the pivot element.
- **pivot**: The existing element in the list that will serve as the reference point for the insertion.
- **element**: The new element to be inserted into the list.

## Return Values

- **(integer)**: The length of the list after the insertion, or -1 if the pivot element was not found.

## Code Examples

```cli
dragonfly> RPUSH mylist "one" "two" "three"
(integer) 3
dragonfly> LINSERT mylist BEFORE "two" "one-and-a-half"
(integer) 4
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "one-and-a-half"
3) "two"
4) "three"
dragonfly> LINSERT mylist AFTER "two" "two-and-a-quarter"
(integer) 5
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "one-and-a-half"
3) "two"
4) "two-and-a-quarter"
5) "three"
dragonfly> LINSERT mylist BEFORE "four" "zero"
(integer) -1
```

## Best Practices

Use `LINSERT` when you need to add elements to a list at specific positions relative to other elements. It is more efficient than retrieving the entire list, modifying it, and writing it back.

## Common Mistakes

- **Pivot Not Found**: If the pivot element does not exist in the list, `LINSERT` will return -1.
- **Non-List Key**: Applying `LINSERT` on a key that is not associated with a list will result in an error.

## FAQs

### What happens if the list does not exist?

If the specified key does not exist, `LINSERT` will behave as if the pivot element was not found and return -1.

### Can I use LINSERT on non-string elements?

Redis lists store strings, so all elements must be string values. Non-string data types must be serialized into strings before using `LINSERT`.

### Is it possible to insert multiple elements at once?

No, `LINSERT` only allows inserting one element at a time relative to the pivot.
