---
description: Execute a read-only Lua script server side
---

# EVAL_RO

## Syntax

    EVAL_RO script numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

This is a read-only variant of the `EVAL` command that cannot execute commands that modify data.

For more information about when to use this command vs `EVAL`, please refer to [Read-only scripts](https://redis.io/docs/manual/programmability/#read-only_scripts).

For more information about `EVAL` scripts please refer to [Introduction to Eval Scripts](https://redis.io/topics/eval-intro).

## Examples

```
> SET mykey "Hello"
OK

> EVAL_RO "return redis.call('GET', KEYS[1])" 1 mykey
"Hello"

> EVAL_RO "return redis.call('DEL', KEYS[1])" 1 mykey
(error) ERR Error running script (call to b0d697da25b13e49157b2c214a4033546aba2104): @user_script:1: @user_script: 1: Write commands are not allowed from read-only scripts.
```
