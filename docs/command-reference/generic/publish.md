---
description: Post a message to a channel
---

# PUBLISH

## Syntax

    PUBLISH channel message

**Time complexity:** O(N+M) where N is the number of clients subscribed to the receiving channel and M is the total number of subscribed patterns (by any client).

Posts a message to the given channel.

In a Redis Cluster clients can publish to every node. The cluster makes sure
that published messages are forwarded as needed, so clients can subscribe to any
channel by connecting to any one of the nodes.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of clients that received the message. Note that in a
Redis Cluster, only clients that are connected to the same node as the
publishing client are included in the count.
