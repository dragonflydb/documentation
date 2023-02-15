---
description: Remove and get the last elements in a list
---

# RPOP

## Syntax

    RPOP key [count]

**Time complexity:** O(N) where N is the number of elements returned

Removes and returns the last elements of the list stored at `key`.

By default, the command pops a single element from the end of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.

## Return

When called without the `count` argument:

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the value of the last element, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of popped elements, or `nil` when `key` does not exist.

## Examples

```cli
RPUSH mylist "one" "two" "three" "four" "five"
RPOP mylist
RPOP mylist 2
LRANGE mylist 0 -1
```
