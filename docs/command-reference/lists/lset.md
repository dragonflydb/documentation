---
description: Understand using Redis LSET command to modify a specified index of a list.
---

import PageTitle from '@site/src/components/PageTitle';

# LSET

<PageTitle title="Redis LSET Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `LSET` command in Redis is used to set the value of an element in a list by its index. This command is useful in scenarios where you need to update an element at a specific position within a list without removing or adding any elements.

## Syntax

```plaintext
LSET key index value
```

## Parameter Explanations

- **key**: The name of the list.
- **index**: The position of the element to be updated. Indexes start from 0 for the head of the list, and can be negative to indicate offsets from the end of the list (e.g., -1 is the last element).
- **value**: The new value to set at the specified index.

## Return Values

- **OK**: If the operation is successful.
- **Error**: If the key does not hold a list, or if the index is out of range.

## Code Examples

```cli
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> LSET mylist 1 "new-value"
OK
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "new-value"
3) "three"
```

## Best Practices

Ensure the index you are targeting exists within the list to avoid errors. Validating the list length before using `LSET` can help maintain robustness.

## Common Mistakes

### Using Out-of-Range Index

Attempting to set an element at an index that doesn't exist will result in an error:

```cli
dragonfly> LSET mylist 10 "undefined"
(error) ERR index out of range
```

### Applying `LSET` on Non-list Types

Trying to use `LSET` on keys that do not store lists will lead to an error:

```cli
dragonfly> SET mystring "hello"
OK
dragonfly> LSET mystring 0 "world"
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

## FAQs

### What happens if I use a negative index?

Negative indexes count from the end of the list. For instance, `-1` refers to the last element, `-2` to the second last, and so on.

### Can `LSET` create a new element if the index doesn't exist?

No, `LSET` only updates existing elements. If the index is out of the current list bounds, it will return an error.
