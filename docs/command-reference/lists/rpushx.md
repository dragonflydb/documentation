---
description: Append an element to a list, only if the list exists
---

# RPUSHX

## Syntax

    RPUSHX key element [element ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

Inserts specified values at the tail of the list stored at `key`, only if `key`
already exists and holds a list.
In contrary to `RPUSH`, no operation will be performed when `key` does not yet
exist.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the length of the list after the push operation.

## Examples

```shell
dragonfly> RPUSH mylist "Hello"
(integer) 1
dragonfly> RPUSHX mylist "World"
(integer) 2
dragonfly> RPUSHX myotherlist "World"
(integer) 0
dragonfly> LRANGE mylist 0 -1
1) "Hello"
2) "World"
dragonfly> LRANGE myotherlist 0 -1

```
