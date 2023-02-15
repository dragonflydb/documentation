---
description: Resume processing of clients that were paused
---

# CLIENT UNPAUSE

## Syntax

    CLIENT UNPAUSE 

**Time complexity:** O(N) Where N is the number of paused clients

`CLIENT UNPAUSE` is used to resume command processing for all clients that were paused by `CLIENT PAUSE`.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): The command returns `OK`
