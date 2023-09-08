---
description: Get the count of subscribers for shard channels
---

# PUBSUB SHARDNUMSUB

## Syntax

    PUBSUB SHARDNUMSUB [shardchannel [shardchannel ...]]

**Time complexity:** O(N) for the SHARDNUMSUB subcommand, where N is the number of requested shard channels

**ACL categories:** @pubsub, @slow

Returns the number of subscribers for the specified shard channels.

Note that it is valid to call this command without channels, in this case it will just return an empty list.

Cluster note: in a Redis Cluster, `PUBSUB`'s replies in a cluster only report information from the node's Pub/Sub context, rather than the entire cluster.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): a list of channels and number of subscribers for every channel.

The format is channel, count, channel, count, ..., so the list is flat. The order in which the channels are listed is the same as the order of the shard channels specified in the command call.

## Examples

```
> PUBSUB SHARDNUMSUB orders
1) "orders"
2) (integer) 1
```
