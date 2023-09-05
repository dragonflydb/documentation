---
description: Remove elements from a list
---

# LREM

## Syntax

    LREM key count element

**Time complexity:** O(N+M) where N is the length of the list and M is the number of elements removed.

**ACL categories:** @write, @list, @slow

Removes the first `count` occurrences of elements equal to `element` from the list
stored at `key`.
The `count` argument influences the operation in the following ways:

* `count > 0`: Remove elements equal to `element` moving from head to tail.
* `count < 0`: Remove elements equal to `element` moving from tail to head.
* `count = 0`: Remove all elements equal to `element`.

For example, `LREM list -2 "hello"` will remove the last two occurrences of
`"hello"` in the list stored at `list`.

Note that non-existing keys are treated like empty lists, so when `key` does not
exist, the command will always return `0`.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of removed elements.

## Examples

```shell
dragonfly> RPUSH mylist "hello"
(integer) 1
dragonfly> RPUSH mylist "hello"
(integer) 2
dragonfly> RPUSH mylist "foo"
(integer) 3
dragonfly> RPUSH mylist "hello"
(integer) 4
dragonfly> LREM mylist -2 "hello"
(integer) 2
dragonfly> LRANGE mylist 0 -1
1) "hello"
2) "foo"
```
