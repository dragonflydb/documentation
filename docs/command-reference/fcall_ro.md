---
description: Invoke a read-only function
---

# FCALL_RO

## Syntax

    FCALL_RO function numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the function that is executed.

This is a read-only variant of the `FCALL` command that cannot execute commands that modify data.

For more information about when to use this command vs `FCALL`, please refer to [Read-only scripts](https://redis.io/docs/manual/programmability/#read-only_scripts).

For more information please refer to [Introduction to Redis Functions](https://redis.io/topics/functions-intro).
