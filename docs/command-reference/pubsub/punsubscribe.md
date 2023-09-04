---
description: Stop listening for messages posted to channels matching the given patterns
---

# PUNSUBSCRIBE

## Syntax

    PUNSUBSCRIBE [pattern [pattern ...]]

**Time complexity:** O(N+M) where N is the number of patterns the client is already subscribed and M is the number of total patterns subscribed in the system (by any client).

**ACL categories:** @pubsub, @slow

Unsubscribes the *client* from the given patterns, or from all of them if none is
given.

When no patterns are specified, the client is unsubscribed from all the
previously subscribed patterns.
In this case, a message for every unsubscribed pattern will be sent to the
client.

## Examples

```shell
user:1> PSUBSCRIBE h[ae]llo
---
dragonfly> PUBLISH hallo message
dragonfly> PUBLISH hello message
---
user:1>
recieved 'message' in hello
recieved 'message' in hallo
user:1> PUNSUBSCRIBE hallo
---
dragonfly> PUBLISH hallo message2
dragonfly> PUBLISH hello message2
---
user:1>
recieved 'message' in hello
```
