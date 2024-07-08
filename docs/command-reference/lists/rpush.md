---
description: Learn how to use Redis RPUSH command for appending a value at the end of a list.
---

import PageTitle from '@site/src/components/PageTitle';

# RPUSH

<PageTitle title="Redis RPUSH Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `RPUSH` command in Redis is used to add one or multiple elements to the tail (right) of a list. This command is useful for maintaining queues, logs, or any ordered data structure where new items need to be added to the end.

## Syntax

```plaintext
RPUSH key element [element ...]
```

## Parameter Explanations

- **key**: The name of the list to which you want to add elements. If the list does not exist, a new list will be created.
- **element**: One or more elements to be added to the list. These can be strings or other types that can be converted to a string representation.

## Return Values

The `RPUSH` command returns an integer representing the length of the list after the push operation.

### Example Outputs:

- Adding a single element to an empty list:
  ```cli
  dragonfly> RPUSH mylist "hello"
  (integer) 1
  ```
- Adding multiple elements:
  ```cli
  dragonfly> RPUSH mylist "world" "!"
  (integer) 3
  ```

## Code Examples

```cli
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three" "four"
(integer) 4
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
3) "three"
4) "four"
```

## Best Practices

- Ensure the list key exists and is of type list before using `RPUSH`. Using `RPUSH` on a key holding a non-list value will result in an error.
- When adding multiple elements at once, include all elements in a single `RPUSH` command to optimize performance.

## Common Mistakes

- Attempting to use `RPUSH` on a key that holds a non-list value results in a type error.
- Not checking the list length after multiple operations could lead to unexpected results if your application logic depends on specific list sizes.

## FAQs

### What happens if the list does not exist?

If the specified key does not exist, `RPUSH` will create a new list with the provided elements.

### Can I use `RPUSH` with non-string values?

Yes, as long as the values can be coerced into a string format, `RPUSH` will accept them.

### Is there a limit to the number of elements I can add with `RPUSH`?

Practically, the number is limited by the available memory on the Redis server. There is no explicit limit set by Redis for the number of elements per `RPUSH` command.
