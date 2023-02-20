---
description: Kill the function currently in execution.
---

# FUNCTION KILL

## Syntax

    FUNCTION KILL 

**Time complexity:** O(1)

Kill a function that is currently executing.


The `FUNCTION KILL` command can be used only on functions that did not modify the dataset during their execution (since stopping a read-only function does not violate the scripting engine's guaranteed atomicity).

For more information please refer to [Introduction to Redis Functions](https://redis.io/topics/functions-intro).

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)
