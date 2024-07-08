---
description: Learn to use Redis RPOPLPUSH to shift elements between two lists and provide basic queueing.
---

import PageTitle from '@site/src/components/PageTitle';

# RPOPLPUSH

<PageTitle title="Redis RPOPLPUSH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`RPOPLPUSH` is a Redis command that atomically removes the last element (tail) from one list and inserts it at the beginning (head) of another list. This operation is useful for implementing circular lists or rotating tasks in task queues.

## Syntax

```plaintext
RPOPLPUSH source destination
```

## Parameter Explanations

- `source`: The name of the list from which to pop the element. This parameter must be an existing list.
- `destination`: The name of the list to push the popped element onto. This can be the same as the source list, effectively rotating the list.

## Return Values

- Returns the element being popped and pushed.
- If the `source` list is empty, a nil value is returned.

## Code Examples

```cli
dragonfly> LPUSH mylist "one"
(integer) 1
dragonfly> LPUSH mylist "two"
(integer) 2
dragonfly> LPUSH mylist "three"
(integer) 3
dragonfly> LRANGE mylist 0 -1
1) "three"
2) "two"
3) "one"
dragonfly> RPOPLPUSH mylist myotherlist
"one"
dragonfly> LRANGE mylist 0 -1
1) "three"
2) "two"
dragonfly> LRANGE myotherlist 0 -1
1) "one"
dragonfly> RPOPLPUSH mylist mylist
"two"
dragonfly> LRANGE mylist 0 -1
1) "two"
2) "three"
```

## Best Practices

Using `RPOPLPUSH` can help maintain the order of tasks when working with task queues. It ensures atomic operations, preventing race conditions in concurrent environments.

## Common Mistakes

### Using Non-List Data Types

Trying to use `RPOPLPUSH` on keys that are not lists will result in an error. Ensure both `source` and `destination` are lists.

### Popping from Empty Lists

If the `source` list is empty, `RPOPLPUSH` will return a nil value. Handle this scenario to avoid unexpected behaviors in your application logic.

## FAQs

### Can `RPOPLPUSH` Be Used on the Same List?

Yes, `RPOPLPUSH` can be used on the same list to rotate its elements.

### What Happens if the Source List is Empty?

If the source list is empty, `RPOPLPUSH` returns nil and no operation is performed on the destination list.
