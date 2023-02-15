---
description: Execute a read-only Lua script server side
---

# EVALSHA_RO

## Syntax

    EVALSHA_RO sha1 numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

This is a read-only variant of the `EVALSHA` command that cannot execute commands that modify data.

For more information about when to use this command vs `EVALSHA`, please refer to [Read-only scripts](https://redis.io/docs/manual/programmability/#read-only_scripts).

For more information about `EVALSHA` scripts please refer to [Introduction to Eval Scripts](https://redis.io/topics/eval-intro).
