---
description: Remove and get the first elements in a list
---

# LPOP

## Syntax

    LPOP key [count]

**Time complexity:** O(N) where N is the number of elements returned

Removes and returns the first elements of the list stored at `key`.

By default, the command pops a single element from the beginning of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.

## Return

When called without the `count` argument:

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): the value of the first element, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of popped elements, or `nil` when `key` does not exist.

## Examples

```cli
RPUSH mylist "one" "two" "three" "four" "five"
LPOP mylist
LPOP mylist 2
LRANGE mylist 0 -1
```
