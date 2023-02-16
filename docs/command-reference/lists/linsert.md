---
description: Insert an element before or after another element in a list
---

# LINSERT

## Syntax

    LINSERT key <BEFORE | AFTER> pivot element

**Time complexity:** O(N) where N is the number of elements to traverse before seeing the value pivot. This means that inserting somewhere on the left end on the list (head) can be considered O(1) and inserting somewhere on the right end (tail) is O(N).

Inserts `element` in the list stored at `key` either before or after the reference
value `pivot`.

When `key` does not exist, it is considered an empty list and no operation is
performed.

An error is returned when `key` exists but does not hold a list value.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the list length after a successful insert operation, `0` if the `key` doesn't exist, and `-1` when the `pivot` wasn't found.

## Examples

```cli
RPUSH mylist "Hello"
RPUSH mylist "World"
LINSERT mylist BEFORE "World" "There"
LRANGE mylist 0 -1
```
