---
description: Return the number of entries in a stream
---

# XLEN

## Syntax

    XLEN key

**Time complexity:** O(1)

Returns the number of entries inside a stream. If the specified key does not
exist the command returns zero, as if the stream was empty.
However note that unlike other Redis types, zero-length streams are
possible, so you should call `TYPE` or `EXISTS` in order to check if
a key exists or not.

Streams are not auto-deleted once they have no entries inside (for instance
after an `XDEL` call), because the stream may have consumer groups
associated with it.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of entries of the stream at `key`.

## Examples

```shell
dragonfly> XADD mystream * item 1
"1676903940326-0"
dragonfly> XADD mystream * item 2
"1676903940327-0"
dragonfly> XADD mystream * item 3
"1676903940327-1"
dragonfly> XLEN mystream
(integer) 3
```
