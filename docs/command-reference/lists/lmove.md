---
description: Learn using Redis LMOVE to shift an element from source list to destination list.
---

import PageTitle from '@site/src/components/PageTitle';

# LMOVE

<PageTitle title="Redis LMOVE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LMOVE` command in Redis atomically moves an element from one list to another, supporting both left and right directions. It's particularly useful for implementing queues or stacks where elements need to be transferred across different lists without race conditions.

## Syntax

```cli
LMOVE source destination LEFT|RIGHT LEFT|RIGHT
```

## Parameter Explanations

- **source**: The key of the list from which the element will be moved.
- **destination**: The key of the list to which the element will be moved.
- **LEFT|RIGHT**: Direction to pop from the source list. `LEFT` pops the first element (head), while `RIGHT` pops the last element (tail).
- **LEFT|RIGHT**: Direction to push to the destination list. `LEFT` pushes the element to the front (head), while `RIGHT` pushes it to the back (tail).

## Return Values

If successful, `LMOVE` returns the element that was moved. If either the source list is empty or does not exist, it returns `nil`.

### Examples of Possible Outputs

1. Element successfully moved:
   ```cli
   "element_value"
   ```
2. Source list is empty/non-existent:
   ```cli
   (nil)
   ```

## Code Examples

```cli
dragonfly> RPUSH mylist "one" "two" "three"
(integer) 3
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
3) "three"
dragonfly> LMOVE mylist myotherlist RIGHT LEFT
"three"
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
dragonfly> LRANGE myotherlist 0 -1
1) "three"
```

## Best Practices

- When using `LMOVE` to implement a task queue, ensure that both the source and destination keys are properly managed to avoid accidental data loss.
- Consider using `BLMOVE` if you need blocking behavior when the source list is empty.

## Common Mistakes

- Forgetting to specify both directions (LEFT|RIGHT) for popping and pushing can lead to syntax errors.
- Using non-list types as source or destination can result in unexpected errors.

## FAQs

### What happens if the source list is empty?

`LMOVE` returns `nil` and no element is moved.

### Can `LMOVE` be used with non-list data types?

No, both the source and destination must be lists.
