---
description:  Learn how to use Redis LPUSH command to insert an element at the start of a list.
---
import PageTitle from '@site/src/components/PageTitle';

# LPUSH

<PageTitle title="Redis LPUSH Command (Documentation) | Dragonfly" />

## Syntax

    LPUSH key element [element ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @list, @fast

Insert all the specified values at the head of the list stored at `key`.
If `key` does not exist, it is created as empty list before performing the push
operations.
When `key` holds a value that is not a list, an error is returned.

It is possible to push multiple elements using a single command call just
specifying multiple arguments at the end of the command.
Elements are inserted one after the other to the head of the list, from the
leftmost element to the rightmost element.
So for instance the command `LPUSH mylist a b c` will result into a list
containing `c` as first element, `b` as second element and `a` as third element.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the length of the list after the push operations.

## Examples

```shell
dragonfly> LPUSH mylist "world"
(integer) 1
dragonfly> LPUSH mylist "hello"
(integer) 2
dragonfly> LRANGE mylist 0 -1
1) "hello"
2) "world"
```
