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

[Array reply](https://valkey.io/docs/latest/develop/reference/protocol-spec/#arrays): an array of integer replies, one per field, in the same order as the fields were requested:

- Integer reply: `-2` if the field does not exist in the hash, or if the hash key itself does not exist.
- Integer reply: `-1` if the field exists but has no associated expiration (it persists indefinitely).
- Integer reply: a positive integer representing the remaining TTL in seconds.

[Simple error reply](https://valkey.io/docs/latest/develop/reference/protocol-spec/#simple-errors):

- If the `FIELDS` argument is missing or not at the correct position, a syntax error is returned.
- If `numfields` does not match the number of field arguments provided, a syntax error is returned.
- If the key exists but is not a hash, a `WRONGTYPE` error is returned.

## Parameters

| Parameter   | Description                                                 |
|-------------|-------------------------------------------------------------|
| `key`       | The hash key to inspect.                                    |
| `numfields` | The number of field names that follow.                      |
| `field`     | One or more field names whose remaining TTL you want to query. |

## Examples

**Fields with no expiry, one non-existent field:**

```shell
dragonfly> HSET myhash field1 "hello" field2 "world"
(integer) 2
dragonfly> HTTL myhash FIELDS 3 field1 field2 nosuchfield
1) (integer) -1
2) (integer) -1
3) (integer) -2
```

**Setting an expiry and checking the remaining TTL:**

```shell
dragonfly> HEXPIRE myhash 30 FIELDS 1 field1
1) (integer) 1
dragonfly> HTTL myhash FIELDS 2 field1 field2
1) (integer) 29
2) (integer) -1
```

**Key does not exist — all fields return `-2`:**

```shell
dragonfly> HTTL no-key FIELDS 2 field1 field2
1) (integer) -2
2) (integer) -2
```

**Wrong key type:**

```shell
dragonfly> SET mystring "value"
"OK"
dragonfly> HTTL mystring FIELDS 1 field1
(error) WRONGTYPE Operation against a key holding the wrong kind of value
```

## Notes

- `HTTL` is a read-only command and does not modify the hash or any field TTLs.
- The reported TTL reflects the time remaining at the moment the command is executed. For precise expiry management, consider the clock resolution on the server.
- To remove an expiry from a field (make it persist), re-set the field without an expiry using [`HSET`](./hset.md).
- For millisecond precision, use the `HPTTL` command when it becomes available.

## Related Commands

- [`HEXPIRE`](./hexpire.md) — Set a TTL on one or more hash fields.
- [`HSETEX`](./hsetex.md) — Set hash field values along with a TTL.
- [`HSET`](./hset.md) — Set hash field values (no expiry).
- [`HGETALL`](./hgetall.md) — Retrieve all fields and values of a hash.
