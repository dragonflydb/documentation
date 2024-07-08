---
description: Discover how to use Redis RPOP command to remove and fetch the last element of a list.
---

import PageTitle from '@site/src/components/PageTitle';

# RPOP

<PageTitle title="Redis RPOP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `RPOP` command in Redis is used to remove and return the last element of a list. This is particularly useful in scenarios where you need to process items in a Last-In-First-Out (LIFO) order, such as stack operations or task processing queues.

## Syntax

```plaintext
RPOP key
```

## Parameter Explanations

- **key**: The name of the list from which the last element will be removed and returned. If the key does not exist or the list is empty, `RPOP` returns `nil`.

## Return Values

- **String**: The value of the last element that was removed from the list.
- **nil**: Returned when the key does not exist or the list is empty.

Example:

```cli
dragonfly> RPUSH mylist "a" "b" "c"
(integer) 3
dragonfly> RPOP mylist
"c"
dragonfly> RPOP mylist
"b"
dragonfly> RPOP mylist
"a"
dragonfly> RPOP mylist
(nil)
```

## Code Examples

```cli
dragonfly> RPUSH mylist "apple" "banana" "cherry"
(integer) 3
dragonfly> RPOP mylist
"cherry"
dragonfly> LRANGE mylist 0 -1
1) "apple"
2) "banana"
dragonfly> RPOP mylist
"banana"
dragonfly> LRANGE mylist 0 -1
1) "apple"
dragonfly> RPOP mylist
"apple"
dragonfly> RPOP mylist
(nil)
```

## Best Practices

- Ensure that the list exists and has elements before calling `RPOP` to avoid unexpected `nil` responses.
- Consider using `BRPOP` for blocking pops if you need to wait for an item to be available in the list.

## Common Mistakes

- Popping from an empty list or a non-list key, resulting in `nil`.
- Not accounting for `nil` return values in application logic, potentially leading to errors.

## FAQs

### What happens if I use RPOP on a non-list data type?

Using `RPOP` on a non-list data type will result in a type error. Always ensure the key corresponds to a list.

### Can RPOP handle multiple elements at once?

No, `RPOP` removes and returns only one element at a time from the end of the list.
