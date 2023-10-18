---
description:  Learn to use Redis LPUSHX for prepending a value to a list when list exists.
---
import PageTitle from '@site/src/components/PageTitle';

# LPUSHX

<PageTitle title="Redis LPUSHX Command (Documentation) | Dragonfly" />

## Syntax

    LPUSHX key element [element ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @list, @fast

Inserts specified values at the head of the list stored at `key`, only if `key`
already exists and holds a list.
In contrary to `LPUSH`, no operation will be performed when `key` does not yet
exist.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the length of the list after the push operation.

## Examples

```shell
dragonfly> LPUSH mylist "World"
(integer) 1
dragonfly> LPUSHX mylist "Hello"
(integer) 2
dragonfly> LPUSHX myotherlist "Hello"
(integer) 0
dragonfly> LRANGE mylist 0 -1
1) "Hello"
2) "World"
dragonfly> LRANGE myotherlist 0 -1
(empty array)
```
