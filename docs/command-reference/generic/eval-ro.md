---
description: "Learn how to use Redis EVAL_RO command to execute a read-only Lua script."
---

import PageTitle from '@site/src/components/PageTitle';

# EVAL_RO

<PageTitle title="Redis EVAL_RO Command (Documentation) | Dragonfly" />

## Syntax

    EVAL_RO script numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

**ACL categories:** @slow, @scripting

Execute a server-side Lua script in read-only mode.

`EVAL_RO` is identical to `EVAL`, except that the script must not perform any write operations.
Scripts executed via `EVAL_RO` are treated as read-only and may run with different transaction semantics.

The first argument is the script's source code. The second argument is the number of input key name arguments, followed by all the keys accessed by the script. Any additional input arguments should not represent names of keys.

For a general introduction to scripting, see `EVAL` and the [Redis Programmability](https://redis.io/docs/latest/develop/interact/programmability/) docs. For Valkey semantics reference, see the [corresponding command page](https://valkey.io/commands/eval_ro/).

## Return

The reply is the result returned by the script, using the [RESP](https://redis.io/docs/latest/develop/reference/protocol-spec/) types.

## Examples

```shell
dragonfly> SET mykey 1
dragonfly> EVAL_RO "return redis.call('GET', KEYS[1])" 1 mykey
"1"
```

```shell
dragonfly> SET mykey 1
dragonfly> EVAL_RO "redis.call('SET', KEYS[1], 'x'); return 1" 1 mykey
(error) ERR Error running script (call to 32c1c320503641a699eba3c8f1f16cacb98c3393): @user_script:2: Write commands are not allowed from read-only scripts
```

## Notes

- `EVAL_RO` must not modify data. If a script attempts to call mutating commands (e.g., `SET`, `HSET`, `LPUSH`), the server returns an error.
- Keys used by the script must be declared via `numkeys` and subsequent key arguments, same as `EVAL`.
- Dragonfly enforces read-only behavior and may optimize execution accordingly.

## See also

[`EVAL`](./eval.md) | [`EVALSHA`](./evalsha.md) | [`EVALSHA_RO`](./evalsha-ro.md)
