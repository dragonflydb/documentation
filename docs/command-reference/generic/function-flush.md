---
description: Deleting all functions
---

# FUNCTION FLUSH

## Syntax

    FUNCTION FLUSH [ASYNC | SYNC]

**Time complexity:** O(N) where N is the number of functions deleted

Deletes all the libraries.

Unless called with the optional mode argument, the `lazyfree-lazy-user-flush` configuration directive sets the effective behavior. Valid modes are:

* `ASYNC`: Asynchronously flush the libraries.
* `!SYNC`: Synchronously flush the libraries.

For more information please refer to [Introduction to Redis Functions](https://redis.io/topics/functions-intro).

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)
