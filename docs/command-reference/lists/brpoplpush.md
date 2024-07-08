---
description: Understand Redis BRPOPLPUSH for moving an element from one list to another with blocking.
---

import PageTitle from '@site/src/components/PageTitle';

# BRPOPLPUSH

<PageTitle title="Redis BRPOPLPUSH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BRPOPLPUSH` command is used to atomically remove the last element from one list, push it to another list, and return the element. This command is particularly useful in scenarios where lists are being used as work queues. It enables a blocking pop operation with an automatic push, which ensures that tasks can be moved seamlessly between different stages of processing.

## Syntax

```plaintext
BRPOPLPUSH source destination timeout
```

## Parameter Explanations

- `source`: The key of the list from which to pop the last element.
- `destination`: The key of the list to which to push the element.
- `timeout`: The maximum number of seconds to block if the source list is empty. A `timeout` of 0 means to block indefinitely.

## Return Values

- Returns the element that was popped and pushed.
- If the `timeout` expires without any elements being available in the `source` list, it returns `nil`.

## Code Examples

```cli
dragonfly> RPUSH source_list "task1" "task2"
(integer) 2
dragonfly> BRPOPLPUSH source_list destination_list 5
"task2"
dragonfly> LRANGE destination_list 0 -1
1) "task2"
dragonfly> BRPOPLPUSH source_list destination_list 5
"task1"
dragonfly> LRANGE destination_list 0 -1
1) "task2"
2) "task1"
dragonfly> BRPOPLPUSH source_list destination_list 2
(nil)
```

## Best Practices

- Use a reasonable `timeout` to avoid indefinite blocking in production systems.
- Ensure proper handling of `nil` returns to manage timeouts effectively.

## Common Mistakes

- Using the command with non-list data types, which will result in errors.
- Setting too short of a `timeout`, which may lead to frequent nil returns and inefficient processing.

## FAQs

### What happens if the `source` list is empty?

If the `source` list is empty, `BRPOPLPUSH` will block for the specified `timeout`. If no element becomes available within this period, it returns `nil`.

### Can `BRPOPLPUSH` operate across different databases?

No, `BRPOPLPUSH` can only operate within the same database. You cannot use it to move elements between lists in different databases.

### Is `BRPOPLPUSH` atomic?

Yes, `BRPOPLPUSH` is atomic. The operations of popping from the source list and pushing to the destination list happen together without interference from other commands.
