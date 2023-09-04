---
description: Get an element from a list by its index
---

# LINDEX

## Syntax

    LINDEX key index

**Time complexity:** O(N) where N is the number of elements to traverse to get to the element at index. This makes asking for the first or the last element of the list O(1).

**ACL categories:** @read, @list, @slow

Returns the element at index `index` in the list stored at `key`.
The index is zero-based, so `0` means the first element, `1` the second element
and so on.
Negative indices can be used to designate elements starting at the tail of the
list.
Here, `-1` means the last element, `-2` means the penultimate and so forth.

When the value at `key` is not a list, an error is returned.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the requested element, or `nil` when `index` is out of range.

## Examples

```shell
dragonfly> LPUSH mylist "World"
(integer) 1
dragonfly> LPUSH mylist "Hello"
(integer) 2
dragonfly> LINDEX mylist 0
"Hello"
dragonfly> LINDEX mylist -1
"World"
dragonfly> LINDEX mylist 3
(nil)
```
