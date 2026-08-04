---
description: Learn how to use Redis HPEXPIRETIME to retrieve hash-field expiration timestamps in Dragonfly.
---

import PageTitle from '@site/src/components/PageTitle';

# HPEXPIRETIME

<PageTitle title="Redis HPEXPIRETIME Command (Documentation) | Dragonfly" />

## Syntax

    HPEXPIRETIME key FIELDS numfields field [field ...]

**Time complexity:** O(N) where N is the number of requested fields

**ACL categories:** @read, @hash, @fast

Returns the absolute Unix timestamp, in milliseconds, at which each requested
hash field will expire.

:::note Dragonfly expiration precision

Dragonfly stores hash-field expiration times with whole-second resolution.
Positive `HPEXPIRETIME` results are therefore multiples of 1000, even when the
expiration was set with a millisecond-based option such as `HGETEX PXAT`.

:::

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): one integer for each
requested field, in the same order:

- `-2` if the field does not exist or the hash key does not exist.
- `-1` if the field exists but has no expiration.
- A positive integer representing the field's absolute Unix expiration time in
  milliseconds.

An [error reply](https://valkey.io/topics/protocol/#simple-errors) is returned
if `key` contains a non-hash value or the arguments are invalid.

## Examples

Set an expiration on one field, then inspect fields with and without an
expiration:

```shell
dragonfly> HSET account:42 name Alice status active
(integer) 2
dragonfly> HGETEX account:42 EX 3600 FIELDS 1 status
1) "active"
dragonfly> HPEXPIRETIME account:42 FIELDS 3 name status missing
1) (integer) -1
2) (integer) 1785846880000
3) (integer) -2
```

The positive timestamp depends on the server time when the expiration is set.

When the hash key does not exist, every requested field returns `-2`:

```shell
dragonfly> HPEXPIRETIME no-such-key FIELDS 2 first second
1) (integer) -2
2) (integer) -2
```

## See also

[`HGETEX`](./hgetex.md) | [`HEXPIRE`](./hexpire.md) | [`HTTL`](./httl.md)
