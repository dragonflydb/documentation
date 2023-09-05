---
description: Execute a Lua script server side
---

# EVALSHA

## Syntax

    EVALSHA sha1 numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

**ACL categories:** @slow, @scripting

Evaluate a script from the server's cache by its SHA1 digest.

The server caches scripts by using the `SCRIPT LOAD` command.
The command is otherwise identical to `EVAL`.

Please refer to the [Redis Programmability](https://redis.io/topics/programmability) and [Introduction to Eval Scripts](https://redis.io/topics/eval-intro) for more information about Lua scripts.
