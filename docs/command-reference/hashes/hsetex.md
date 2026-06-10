---
description: "Learn how to use Redis HSETEX command to set the value of a hash field and its expiry time. A smart way to manage temporary data."
---

import PageTitle from '@site/src/components/PageTitle';

# HSETEX

<PageTitle title="Redis HSETEX Command (Documentation) | Dragonfly" />

## Syntax

    HSETEX key [NX] [KEEPTTL] seconds field value [field value ...]

**Time complexity:** O(1) for each field/value pair added, so O(N) to add N field/value pairs when the command is called with multiple field/value pairs.

**ACL categories:** @hash, @fast, @write

**Warning:** Experimental! Dragonfly-specific.

Similar to [`HSET`](./hset.md) but adds one or more hash fields that expire after specified number of seconds.
By default, this command overwrites the values and expirations of specified fields that exist in the hash.
If `NX` option is specified, the field data will not be overwritten.
If `KEEPTTL` option is specified, the TTL for the field will not be overwritten.
If `key` doesn't exist, a new key holding a hash is created.

The expiration time can be accessed with the [`FIELDTTL`](../generic/fieldttl.md) command.

## Return

[Integer reply](https://valkey.io/topics/protocol/#integers): The number of fields that were added.

## Examples

Cache a user session with a 30-second TTL on every field:

```shell
dragonfly> HSETEX session:abc 30 user alice role admin
(integer) 2
dragonfly> HGETALL session:abc
1) "user"
2) "alice"
3) "role"
4) "admin"
dragonfly> FIELDTTL session:abc user
(integer) 30
```

Refreshing a field re-sets its TTL. `HSETEX` returns the number of NEW fields
added, not modified, so the second call below replies `0` because `user`
already existed:

```shell
dragonfly> HSETEX session:abc 30 user alice
(integer) 1
dragonfly> HSETEX session:abc 60 user alice-updated
(integer) 0
dragonfly> FIELDTTL session:abc user
(integer) 60
dragonfly> HGET session:abc user
"alice-updated"
```

Use `NX` to set a value only if the field does not yet exist (useful for
write-once flags). `NX` leaves an existing field untouched and replies `0`,
while a brand-new field is added and replies `1`:

```shell
dragonfly> HSETEX session:abc 60 user alice
(integer) 1
dragonfly> HSETEX session:abc NX 60 user bob
(integer) 0
dragonfly> HGET session:abc user
"alice"
dragonfly> HSETEX session:abc NX 60 ip 10.0.0.1
(integer) 1
dragonfly> HGET session:abc ip
"10.0.0.1"
```

Use `KEEPTTL` to update a value without changing its existing expiry — useful
when refreshing data but keeping the original session deadline:

```shell
dragonfly> HSETEX session:abc 60 ip 10.0.0.1
(integer) 1
dragonfly> FIELDTTL session:abc ip
(integer) 60
dragonfly> HSETEX session:abc KEEPTTL 9999 ip 10.0.0.2
(integer) 0
dragonfly> FIELDTTL session:abc ip
(integer) 60
dragonfly> HGET session:abc ip
"10.0.0.2"
```

Note: the `9999` argument is required by the syntax but ignored when `KEEPTTL`
is set — the TTL above stays at `60`.
