---
description:  Discover the use of Redis DECR for decrementing the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECR

<PageTitle title="Redis DECR Command (Documentation) | Dragonfly" />

## Syntax

    DECR key

**Time complexity:** O(1)

**ACL categories:** @write, @string, @fast

Decrements the number stored at `key` by one.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as integer.
This operation is limited to **64 bit signed integers**.

See `INCR` for extra information on increment/decrement operations.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the value of `key` after the decrement

## Examples

```shell
dragonfly> SET mykey "10"
OK
dragonfly> DECR mykey
(integer) 9
dragonfly> SET mykey "234293482390480948029348230948"
OK
dragonfly> DECR mykey
"value is not an integer or out of range"
```
