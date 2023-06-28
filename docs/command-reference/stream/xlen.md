---
description: Get the length of a stream
---

# XLEN

## Syntax

	XLEN key

**Time Complexity:** O(1)

Returns the number of entries inside a stream. If the specified
key does not exist the command returns zero, as if the stream was
empty. Note that a stream can be empty and hence **XLEN** is not
a good option to check if a stream exists.

Streams are not auto-deleted once they have no entries inside
(for instance after an **XDEL** call), because the stream may have
consumer groups associated with it.

## Return
[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers):
the number of entries of the stream at key.

## Example

```shell
dragonfly> XADD mystream * name John
"1623910120014-0"
dragonfly> XADD mystream * name Bob
"1623910194423-0"
dragonfly> XADD mystream * name Alice
"1623910226955-0"
dragonfly> XLEN mystream
(integer) 3
```