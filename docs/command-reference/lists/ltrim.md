---
description: Trim a list to the specified range
---

# LTRIM

## Syntax

    LTRIM key start stop

**Time complexity:** O(N) where N is the number of elements to be removed by the operation.

**ACL categories:** @write, @list, @slow

Trim an existing list so that it will contain only the specified range of
elements specified.
Both `start` and `stop` are zero-based indexes, where `0` is the first element
of the list (the head), `1` the next element and so on.

For example: `LTRIM foobar 0 2` will modify the list stored at `foobar` so that
only the first three elements of the list will remain.

`start` and `end` can also be negative numbers indicating offsets from the end
of the list, where `-1` is the last element of the list, `-2` the penultimate
element and so on.

Out of range indexes will not produce an error: if `start` is larger than the
end of the list, or `start > end`, the result will be an empty list (which
causes `key` to be removed).
If `end` is larger than the end of the list, Dragonfly will treat it like the last
element of the list.

A common use of `LTRIM` is together with `LPUSH` / `RPUSH`.
For example:

```
LPUSH mylist someelement
LTRIM mylist 0 99
```

This pair of commands will push a new element on the list, while making sure
that the list will not grow larger than 100 elements. It is important to note that when
used in this way `LTRIM` is an O(1) operation, because in the average case just one element
is removed from the tail of the list.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)

## Examples

```shell
dragonfly> RPUSH mylist "one"
(integer) 1
dragonfly> RPUSH mylist "two"
(integer) 2
dragonfly> RPUSH mylist "three"
(integer) 3
dragonfly> LTRIM mylist 1 -1
"OK"
dragonfly> LRANGE mylist 0 -1
1) "two"
2) "three"
```
