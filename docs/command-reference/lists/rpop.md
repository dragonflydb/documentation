---
description:  Discover how to use Redis RPOP command to remove and fetch the last element of a list.
---
import PageTitle from '@site/src/components/PageTitle';

# RPOP

<PageTitle title="Redis RPOP Command (Documentation) | Dragonfly" />

## Syntax

    RPOP key [count]

**Time complexity:** O(N) where N is the number of elements returned

**ACL categories:** @write, @list, @fast

Removes and returns the last elements of the list stored at `key`.

By default, the command pops a single element from the end of the list.
When provided with the optional `count` argument, the reply will consist of up
to `count` elements, depending on the list's length.

## Return

When called without the `count` argument:

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the value of the last element, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): list of popped elements, or `nil` when `key` does not exist.

## Examples

```shell
dragonfly> RPUSH mylist "one" "two" "three" "four" "five"
(integer) 5
dragonfly> RPOP mylist
"five"
dragonfly> RPOP mylist 2
1) "four"
2) "three"
dragonfly> LRANGE mylist 0 -1
1) "one"
2) "two"
```
