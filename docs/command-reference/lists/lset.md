---
description: Set the value of an element in a list by its index
---

# LSET

## Syntax

    LSET key index element

**Time complexity:** O(N) where N is the length of the list. Setting either the first or the last element of the list is O(1).

Sets the list element at `index` to `element`.
For more information on the `index` argument, see `LINDEX`.

An error is returned for out of range indexes.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)

## Examples

```cli
RPUSH mylist "one"
RPUSH mylist "two"
RPUSH mylist "three"
LSET mylist 0 "four"
LSET mylist -2 "five"
LRANGE mylist 0 -1
```
