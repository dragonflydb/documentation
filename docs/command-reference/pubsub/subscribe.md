---
description: Listen for messages published to the given channels
---

# SUBSCRIBE

## Syntax

    SUBSCRIBE channel [channel ...]

**Time complexity:** O(N) where N is the number of channels to subscribe to.

**ACL categories:** @pubsub, @slow

Subscribes the client to the specified channels.

Once the client enters the subscribed state it is not supposed to issue any
other commands, except for additional `SUBSCRIBE`, `SSUBSCRIBE`, `PSUBSCRIBE`, `UNSUBSCRIBE`, `SUNSUBSCRIBE`, 
`PUNSUBSCRIBE`, `PING`, `RESET` and `QUIT` commands.

## Examples

```shell
user:1> SUBSCRIBE ab[c]
---
dragonfly> PUBLISH abc message
(integer) 0
dragonfly> PUBLISH ab*c message
(integer) 0
dragonfly PUBLISH ab[c] message
(integer) 1
```

