---
description:  Learn how to use Redis DECRBY to decrease the integer value of a key.
---

import PageTitle from '@site/src/components/PageTitle';

# DECRBY

<PageTitle title="Redis DECRBY Command (Documentation) | Dragonfly" />

## Syntax

    DECRBY key decrement

**Time complexity:** O(1)

**ACL categories:** @write, @string, @fast

Decrements the number stored at `key` by `decrement`.
If the key does not exist, it is set to `0` before performing the operation.
An error is returned if the key contains a value of the wrong type or contains a
string that can not be represented as integer.
This operation is limited to 64 bit signed integers.

See `INCR` for extra information on increment/decrement operations.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the value of `key` after the decrement

## Examples

```shell
dragonfly> SET mykey "10"
"OK"
dragonfly> DECRBY mykey 3
(integer) 7
```
