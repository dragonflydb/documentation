---
description:  Learn how to use Redis PUBSUB NUMSUB to get a count of subscriptions for specific channels in your Pub/Sub system.
---
import PageTitle from '@site/src/components/PageTitle';

# PUBSUB NUMSUB

<PageTitle title="Redis PUBSUB NUMSUB Command (Documentation) | Dragonfly" />

## Syntax

    PUBSUB NUMSUB [channel [channel ...]]

**Time complexity:** O(N) for the NUMSUB subcommand, where N is the number of requested channels

**ACL categories:** @pubsub, @slow

Returns the number of subscribers (exclusive of clients subscribed to patterns) for the specified channels.

Note that it is valid to call this command without channels. In this case it will just return an empty list.

Cluster note: in a Redis Cluster clients can subscribe to every node, and can also publish to every other node. The cluster will make sure that published messages are forwarded as needed. That said, `PUBSUB`'s replies in a cluster only report information from the node's Pub/Sub context, rather than the entire cluster.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of channels and number of subscribers for every channel.

The format is channel, count, channel, count, ..., so the list is flat. The order in which the channels are listed is the same as the order of the channels specified in the command call.
