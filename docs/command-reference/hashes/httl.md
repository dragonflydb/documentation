---
description: "Learn how to use the HTTL command to query the remaining TTL of individual fields within a Redis hash, enabling granular cache management."
---

import PageTitle from '@site/src/components/PageTitle';

# HTTL

<PageTitle title="Redis HTTL Command (Documentation) | Dragonfly" />

## Syntax

    HTTL key FIELDS numfields field [field ...]

**Time complexity:** O(N) where N is the number of fields being queried

**ACL categories:** @read, @hash, @fast

Returns the remaining Time-To-Live (TTL) in seconds for one or more fields of a hash stored at `key`.
This allows you to inspect when individual hash fields will expire without modifying them.

Unlike `TTL`, which operates at the key level, `HTTL` operates at the field level.
Field-level expiry is set via [`HEXPIRE`](./hexpire.md) or [`HSETEX`](./hsetex.md).

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): an array of integer replies, one per field, in the same order as the fields were requested:

- Integer reply: `-2` if the field does not exist in the hash, or if the hash key itself does not exist.
- Integer reply: `-1` if the field exists but has no associated expiration (it persists indefinitely).
- Integer reply: a positive integer representing the remaining TTL in seconds.

## Examples

Build a session hash and inspect its per-field TTLs. Some fields have no
expiry, some do, and one is missing entirely:

```shell
dragonfly> HSET session:1 user "alice" role "admin" temp_token "xyz"
(integer) 3
dragonfly> HEXPIRE session:1 600 FIELDS 1 temp_token
1) (integer) 1
dragonfly> HTTL session:1 FIELDS 4 user role temp_token nosuch
1) (integer) -1
2) (integer) -1
3) (integer) 600
4) (integer) -2
```

`user` and `role` exist but have no TTL set (`-1`). `temp_token` expires in 600
seconds. `nosuch` does not exist in the hash (`-2`).

When the hash key itself does not exist, every queried field returns `-2`:

```shell
dragonfly> HTTL no-such-key FIELDS 2 a b
1) (integer) -2
2) (integer) -2
```

Calling `HTTL` on a non-hash key fails with `WRONGTYPE`:

```shell
dragonfly> SET plain-key "hello"
OK
dragonfly> HTTL plain-key FIELDS 1 field
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```
## Notes

- `HTTL` is a read-only command and does not modify the hash or any field TTLs.
- The reported TTL reflects the time remaining at the moment the command is executed. For precise expiry management, consider the clock resolution on the server.
- To remove an expiry from a field (make it persist), re-set the field without an expiry using [`HSET`](./hset.md).

## Related Commands

- [`HEXPIRE`](./hexpire.md) — Set a TTL on one or more hash fields.
- [`FIELDTTL`](../generic/fieldttl.md) — Retrieve the TTL of a specific field.
- [`HSETEX`](./hsetex.md) — Set hash field values along with a TTL.
- [`HSET`](./hset.md) — Set hash field values (no expiry).
- [`HGETALL`](./hgetall.md) — Retrieve all fields and values of a hash.
