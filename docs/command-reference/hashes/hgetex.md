---
description: Learn how to use Redis HGETEX to retrieve hash fields and update their expiration in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# HGETEX

<PageTitle title="Redis HGETEX Command (Documentation) | Dragonfly" />

## Syntax

    HGETEX key [EX seconds | PX milliseconds | EXAT unix-time-seconds | PXAT unix-time-milliseconds | PERSIST] FIELDS numfields field [field ...]

**Time complexity:** O(N) where N is the number of requested fields

**ACL categories:** @write, @hash, @fast

Returns the values of one or more hash fields and optionally changes their
expiration. Without an expiration option, `HGETEX` behaves like
[`HMGET`](./hmget.md) and leaves existing field expirations unchanged.

## Options

| Option | Description |
|---|---|
| `EX seconds` | Set a relative expiration in seconds. |
| `PX milliseconds` | Set a relative expiration in milliseconds. |
| `EXAT unix-time-seconds` | Set an absolute Unix expiration time in seconds. |
| `PXAT unix-time-milliseconds` | Set an absolute Unix expiration time in milliseconds. |
| `PERSIST` | Remove the expiration from the requested fields. |

The options are mutually exclusive and must appear before `FIELDS`. An `EX` or
`PX` value of `0`, or an `EXAT` or `PXAT` value in the past, returns the current
field values and then deletes those fields. If the last field is deleted, the
hash key is also removed.

:::note Dragonfly expiration precision

Dragonfly stores hash-field expiration times with whole-second resolution.
`PX` and `PXAT` accept millisecond values, but the resulting expiration is
quantized to whole-second resolution. Positive values returned by
[`HPEXPIRETIME`](./hpexpiretime.md) are therefore multiples of 1000.
Expirations more than `2^28 - 1` seconds (about 8.5 years) in the future are
rejected.

:::

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): one value for each
requested field, in the same order. A missing field, or every field requested
from a missing key, is returned as `nil`.

An [error reply](https://valkey.io/topics/protocol/#simple-errors) is returned
if `key` contains a non-hash value or the arguments are invalid.

## Examples

Set a TTL while retrieving fields. A missing field is returned as `nil`:

```shell
dragonfly> HSET session:42 user alice token abc
(integer) 2
dragonfly> HGETEX session:42 EX 600 FIELDS 2 token missing
1) "abc"
2) (nil)
```

Remove the field expiration with `PERSIST`:

```shell
dragonfly> HSET session:42 token abc
(integer) 1
dragonfly> HGETEX session:42 EX 600 FIELDS 1 token
1) "abc"
dragonfly> HGETEX session:42 PERSIST FIELDS 1 token
1) "abc"
dragonfly> HTTL session:42 FIELDS 1 token
1) (integer) -1
```

## See also

[`HMGET`](./hmget.md) | [`HSETEX`](./hsetex.md) | [`HEXPIRE`](./hexpire.md) | [`HTTL`](./httl.md) | [`HPEXPIRETIME`](./hpexpiretime.md)
