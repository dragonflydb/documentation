---
description: "Learn how to use the Redis SCRIPT FLUSH command to remove all Lua scripts from the Dragonfly script cache."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT FLUSH

<PageTitle title="Redis SCRIPT FLUSH Command (Documentation) | Dragonfly" />

## Syntax

    SCRIPT FLUSH

**Time complexity:** O(N) with N being the number of scripts in the cache.

**ACL categories:** @scripting, @slow

Flush the Lua scripts cache.
After the flush, `EVALSHA` and `EVALSHA_RO` reply `NOSCRIPT No matching script. Please use EVAL.` for every flushed script,
until the script is loaded again with `SCRIPT LOAD` or run with `EVAL`.

Dragonfly always flushes the cache synchronously: the scripts are removed before `OK` is returned.
Unlike [Valkey](https://valkey.io/commands/script-flush/), Dragonfly does not implement the `ASYNC` and `SYNC` modifiers.
It ignores any arguments after `FLUSH`, so `SCRIPT FLUSH ASYNC` also flushes synchronously and does not return an error.

`SCRIPT FLUSH` also discards the flags set with `SCRIPT FLAGS`, including flags set for scripts that are not loaded yet.
Flags declared in the script body or with `--default_lua_flags` apply again when the script is loaded.
See [Script flags](../../managing-dragonfly/scripting.md#script-flags).

For more information about `EVAL` scripts please refer to [Introduction to Eval Scripts](https://valkey.io/topics/eval-intro/).

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK`.

## Examples

```shell
dragonfly> SCRIPT LOAD "return 1"
"e0e1f9fabfc9d4800c877a703b823ac0578ff8db"
dragonfly> SCRIPT EXISTS e0e1f9fabfc9d4800c877a703b823ac0578ff8db
1) (integer) 1
dragonfly> SCRIPT FLUSH
OK
dragonfly> SCRIPT EXISTS e0e1f9fabfc9d4800c877a703b823ac0578ff8db
1) (integer) 0
```
