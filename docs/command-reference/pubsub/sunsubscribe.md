---
description:  Learn how to use SUNSUBSCRIBE to stop receiving messages published on specific channels in your Pub/Sub setup.
---
import PageTitle from '@site/src/components/PageTitle';

# SUNSUBSCRIBE

<PageTitle title="SUNSUBSCRIBE Command (Documentation) | Dragonfly" />

## Syntax

    SUNSUBSCRIBE [shard_channel [shard_channel ...]]

**Time complexity:** O(N) where N is the number of clients already subscribed to a shard channel.

**ACL categories:** @pubsub, @slow

Unsubscribes the client from the given shard channels, or from all of them if no arguments are given.
For each shard channel a message will be sent to the client.
