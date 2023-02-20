---
description: Return a range of elements in a stream, with IDs matching the
  specified IDs interval, in reverse order (from greater to smaller IDs)
  compared to XRANGE
---

# XREVRANGE

## Syntax

    XREVRANGE key end start [COUNT count]

**Time complexity:** O(N) with N being the number of elements returned. If N is constant (e.g. always asking for the first 10 elements with COUNT), you can consider it O(1).

This command is exactly like `XRANGE`, but with the notable difference of
returning the entries in reverse order, and also taking the start-end
range in reverse order: in `XREVRANGE` you need to state the *end* ID
and later the *start* ID, and the command will produce all the element
between (or exactly like) the two IDs, starting from the *end* side.

So for instance, to get all the elements from the higher ID to the lower
ID one could use:

    XREVRANGE somestream + -

Similarly to get just the last element added into the stream it is
enough to send:

    XREVRANGE somestream + - COUNT 1

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays), specifically:

The command returns the entries with IDs matching the specified range,
from the higher ID to the lower ID matching.
The returned entries are complete, that means that the ID and all the fields
they are composed are returned. Moreover the entries are returned with
their fields and values in the exact same order as `XADD` added them.

## Examples

```shell
dragonfly> XADD writers * name Virginia surname Woolf
"1676903941132-0"
dragonfly> XADD writers * name Jane surname Austen
"1676903941132-1"
dragonfly> XADD writers * name Toni surname Morrison
"1676903941132-2"
dragonfly> XADD writers * name Agatha surname Christie
"1676903941133-0"
dragonfly> XADD writers * name Ngozi surname Adichie
"1676903941133-1"
dragonfly> XLEN writers
(integer) 5
dragonfly> XREVRANGE writers + - COUNT 1
1) 1) "1676903941133-1"
2) 1) "name"
2) "Ngozi"
3) "surname"
4) "Adichie"
```
