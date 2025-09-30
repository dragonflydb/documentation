---
description: Learn how to use Redis BLMOVE to atomically pop from one list and push to another in a blocking way.
---

import PageTitle from '@site/src/components/PageTitle';

# BLMOVE

<PageTitle title="Redis BLMOVE Command (Documentation) | Dragonfly" />

## Syntax

    BLMOVE source destination <LEFT | RIGHT> <LEFT | RIGHT> timeout

**Time complexity:** O(1)

**ACL categories:** @write, @list, @slow, @blocking

`BLMOVE` is the blocking variant of `LMOVE`. If the source list contains elements, the command behaves like   [
`LMOVE`](lmove.md).

If the `source` list is empty or does not exist, the connected client will be blocked until another client pushes an
element to `source`, or until the specified `timeout` is reached.

- A `timeout` of `0` blocks indefinitely until an element is available.
- If the `timeout` expires without an element becoming available, the command returns `nil` and no element is moved.

See also: [`LMOVE`](lmove.md) for the command options.

## Return

* [Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the element being
  popped from `source` and pushed to `destination`, when successful.
* [Nil reply](https://redis.io/docs/latest/develop/reference/protocol-spec#bulk-strings) when the command times out.

## Examples

### Moving an Element

```shell
dragonfly> RPUSH src a b c
(integer) 3
dragonfly> RPUSH dst x y
(integer) 2
dragonfly> BLMOVE src dst RIGHT LEFT 0
"c"
dragonfly> LRANGE src 0 -1
1) "a"
2) "b"
dragonfly> LRANGE dst 0 -1
1) "c"
2) "x"
3) "y"
```

### Blocking with Non-Zero Timeout

```shell
dragonfly> DEL src dst
(integer) 0
dragonfly> BLMOVE empty dst LEFT RIGHT 1.5
(nil)
```
