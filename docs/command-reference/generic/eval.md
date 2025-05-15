---
description: "Learn how to use Redis EVAL command to execute a Lua script."
---

import PageTitle from '@site/src/components/PageTitle';

# EVAL

<PageTitle title="Redis EVAL Command (Documentation) | Dragonfly" />

## Syntax

    EVAL script numkeys [key [key ...]] [arg [arg ...]]

**Time complexity:** Depends on the script that is executed.

**ACL categories:** @slow, @scripting

Invoke the execution of a server-side Lua script.

The first argument is the script's source code.
Scripts are written in [Lua](https://lua.org) and executed by the embedded [Lua 5.4.4](https://redis.io/docs/latest/develop/interact/programmability/lua-api/) interpreter in Dragonfly.

The second argument is the number of input key name arguments, followed by all the keys accessed by the script.
These names of input keys are available to the script as the [_KEYS_ global runtime variable](https://redis.io/docs/latest/develop/interact/programmability/lua-api/#the-keys-global-variable)
Any additional input arguments **should not** represent names of keys.

**Important:**
to ensure the correct execution of scripts, all names of keys that a script accesses must be explicitly provided as input key arguments.
The script **should only** access keys whose names are given as input arguments.
Scripts **should never** access keys with programmatically-generated names or based on the contents of data structures stored in the datastore.

Please refer to the [Redis Programmability](https://redis.io/docs/latest/develop/interact/programmability/) and [Introduction to Eval Scripts](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/) for more information about Lua scripts.

## Examples

The following example will run a script that returns the first argument that it gets.

```shell
dragonfly>  EVAL "return ARGV[1]" 0 hello
"hello"
```
