---
description: "Get insights on Redis EVALSHA command for executing Lua scripts using SHA-1."
---

import PageTitle from '@site/src/components/PageTitle';

# EVALSHA

<PageTitle title="Redis EVALSHA Command (Documentation) | Dragonfly" />

## Syntax

    EVALSHA sha1 numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

**ACL categories:** @slow, @scripting

Evaluate a script from the server's cache by its SHA1 digest.

The server caches scripts by using the `SCRIPT LOAD` command.
The command is otherwise identical to `EVAL`.

Please refer to the [Redis Programmability](https://redis.io/docs/latest/develop/interact/programmability/) and [Introduction to Eval Scripts](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/) for more information about Lua scripts.

## See also

[`EVAL`](./eval.md) | [`EVAL_RO`](./eval-ro.md) | [`EVALSHA_RO`](./evalsha-ro.md)
