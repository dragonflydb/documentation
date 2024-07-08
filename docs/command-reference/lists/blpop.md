---
description: Learn how to use Redis BLPOP to fetch and remove first element from list in blocking way.
---

import PageTitle from '@site/src/components/PageTitle';

# BLPOP

<PageTitle title="Redis BLPOP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `BLPOP` command is used in Redis to remove and return the first element of a list, or block until one is available. It's commonly used in scenarios where you need to implement queues and want to wait for elements to become available.

## Syntax

```cli
BLPOP key [key ...] timeout
```

## Parameter Explanations

- **key**: One or more keys of the lists from which to pop elements.
- **timeout**: The maximum number of seconds to block if no elements are present. A timeout of 0 means to block indefinitely.

## Return Values

`BLPOP` returns a two-element array where the first element is the name of the key where an element was popped, and the second element is the value of the popped element. If the timeout expires, it returns a `nil`.

Example outputs:

- When an element is successfully popped:
  ```cli
  1) "mylist"
  2) "element"
  ```
- When the timeout expires with no elements available:
  ```cli
  (nil)
  ```

## Code Examples

```cli
dragonfly> LPUSH mylist "element1"
(integer) 1
dragonfly> LPUSH mylist "element2"
(integer) 2
dragonfly> BLPOP mylist 0
1) "mylist"
2) "element2"
dragonfly> BLPOP mylist 0
1) "mylist"
2) "element1"
dragonfly> BLPOP mylist 1
(nil)
```

## Best Practices

- Use reasonable timeout values to avoid long blocking times that could impact performance.
- Combine multiple lists in a single `BLPOP` command to monitor multiple queues effectively.

## Common Mistakes

- Blocking with a very short timeout may result in frequent empty responses and inefficient polling.
- Using `BLPOP` on non-list data types will result in an error.

## FAQs

### What happens if the list is empty when BLPOP is called?

If the list is empty, `BLPOP` will block for the specified timeout period or until an element becomes available.

### Can BLPOP handle multiple keys?

Yes, `BLPOP` can be used with multiple keys. It will return as soon as any of the specified keys has an element to pop.
