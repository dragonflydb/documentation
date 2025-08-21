---
description:  Learn how to use Redis RPUSH command for appending a value at the end of a list.
---
import PageTitle from '@site/src/components/PageTitle';

# RPUSH

<PageTitle title="Redis RPUSH Command (Documentation) | Dragonfly" />

## Syntax

    RPUSH key element [element ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @list, @fast 

Insert all the specified values at the tail of the list stored at `key`.
If `key` does not exist, it is created as empty list before performing the push
operation.
When `key` holds a value that is not a list, an error is returned.

It is possible to push multiple elements using a single command call just
specifying multiple arguments at the end of the command.
Elements are inserted one after the other to the tail of the list, from the
leftmost element to the rightmost element.
So for instance the command `RPUSH mylist a b c` will result into a list
containing `a` as first element, `b` as second element and `c` as third element.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the length of the list after the push operation.

## Examples

```shell
dragonfly> RPUSH mylist "hello"
(integer) 1
dragonfly> RPUSH mylist "world"
(integer) 2
dragonfly> LRANGE mylist 0 -1
1) "hello"
2) "world"
```
