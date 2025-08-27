---
description: "Execute cached Lua script in read-only mode by SHA1."
---

import PageTitle from '@site/src/components/PageTitle';

# EVALSHA_RO

<PageTitle title="Redis EVALSHA_RO Command (Documentation) | Dragonfly" />

## Syntax

    EVALSHA_RO sha1 numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

**ACL categories:** @slow, @scripting

Evaluate a script from the server's cache by its SHA1 digest in read-only mode.

`EVALSHA_RO` is identical to `EVALSHA`, except that the script must not perform any write operations. Scripts executed via `EVALSHA_RO` are treated as read-only and may run with different transaction semantics.

The first argument is the script's SHA1 digest as returned by `SCRIPT LOAD`. The second argument is the number of input key name arguments, followed by all the keys accessed by the script. Any additional input arguments should not represent names of keys.

For a general introduction to scripting, see `EVAL` and the Redis Programmability docs. For Valkey semantics reference, see the corresponding command page at `https://valkey.io/commands/evalsha_ro/`.

## Return

The reply is the result returned by the script, using the [RESP](https://redis.io/docs/latest/develop/reference/protocol-spec/) types.

## Examples

```shell
dragonfly> SET mykey 1
OK
dragonfly> SCRIPT LOAD "return redis.call('GET', KEYS[1])"
"<sha1>"
dragonfly> EVALSHA_RO <sha1> 1 mykey
"1"
```

```shell
dragonfly> SCRIPT LOAD "redis.call('SET', KEYS[1], 'x'); return 1"
"<sha1>"
dragonfly> EVALSHA_RO <sha1> 1 mykey
(error) ERR Error running script ... Write commands are not allowed from read-only scripts
```

## Notes

- `EVALSHA_RO` must not modify data. If a script attempts to call mutating commands (e.g., `SET`, `HSET`, `LPUSH`), the server returns an error.
- Keys used by the script must be declared via `numkeys` and subsequent key arguments, same as `EVAL`/`EVALSHA`.
- Dragonfly enforces read-only behavior and may optimize execution accordingly.

## See also

[`EVAL`](./eval.md) | [`EVAL_RO`](./eval-ro.md) | [`EVALSHA`](./evalsha.md)


