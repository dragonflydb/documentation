---
description: Stop listening for messages posted to the given shard channels
---

# SUNSUBSCRIBE

## Syntax

    SUNSUBSCRIBE [shardchannel [shardchannel ...]]

**Time complexity:** O(N) where N is the number of clients already subscribed to a shard channel.

Unsubscribes the client from the given shard channels, or from all of them if none is given.

When no shard channels are specified, the client is unsubscribed from all the previously subscribed shard channels. 
In this case a message for every unsubscribed shard channel will be sent to the client. 

Note: The global channels and shard channels needs to be unsubscribed from separately.

For more information about sharded Pub/Sub, see [Sharded Pub/Sub](https://redis.io/topics/pubsub#sharded-pubsub).
