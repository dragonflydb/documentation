---
description: Learn how to use the Redis BRPOP command to remove and fetch the last element from list.
---

import PageTitle from '@site/src/components/PageTitle';

# BRPOP

<PageTitle title="Redis BRPOP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`BRPOP` is a blocking list pop primitive in Redis. It is used to remove and return the last element of one or more lists, blocking until an element becomes available if none are currently present. This command is particularly useful for implementing queues or task processing systems where consumers wait for tasks to be enqueued.

## Syntax

```plaintext
BRPOP key [key ...] timeout
```

## Parameter Explanations

- **key [key ...]**: One or more keys identifying the lists to be popped from.
- **timeout**: The maximum number of seconds to block. A timeout of 0 can be used to block indefinitely.

## Return Values

- If an element is available, it returns an array with two elements:
  - The first element is the name of the key from which the value was popped.
  - The second element is the value of the popped element.
- If the timeout is reached without a value becoming available, it returns `nil`.

Example outputs:

1. When an element is available:

   ```plaintext
   1) "mylist"
   2) "last_element"
   ```

2. When the timeout is reached:
   ```plaintext
   (nil)
   ```

## Code Examples

```cli
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> BRPOP mylist 0
1) "mylist"
2) "three"
dragonfly> BRPOP mylist 5
1) "mylist"
2) "two"
dragonfly> BRPOP mylist 1
1) "mylist"
2) "one"
dragonfly> BRPOP mylist 1
(nil)
```

## Best Practices

- Use `BRPOP` when implementing consumer-producer models in which consumers need to wait for new items.
- Ensure you handle nil responses appropriately to avoid infinite waiting loops in your application logic.

## Common Mistakes

- Not considering the impact of setting an indefinite timeout (0) on resource utilization.
- Forgetting that `BRPOP` removes the element from the list; if you need to preview without removal, use other commands like `LRANGE`.

## FAQs

### What happens if multiple clients are blocked on a BRPOP and an element becomes available?

The first client that was blocked will receive the element and continue execution. Other clients remain blocked until another element becomes available.

### Can BRPOP be used with multiple lists?

Yes, `BRPOP` can be applied to multiple lists. It will check each list in the order they are given and return as soon as an element is available from any of them.
