---
description: List active shard channels
---

# PUBSUB SHARDCHANNELS

## Syntax

    PUBSUB SHARDCHANNELS [pattern]

**Time complexity:** O(N) where N is the number of active shard channels, and assuming constant time pattern matching (relatively short shard channels).

Lists the currently *active shard channels*.

An active shard channel is a Pub/Sub shard channel with one or more subscribers.

If no `pattern` is specified, all the channels are listed, otherwise if pattern is specified only channels matching the specified glob-style pattern are listed.

The information returned about the active shard channels are at the shard level and not at the cluster level.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a list of active channels, optionally matching the specified pattern.

## Examples

```
> PUBSUB SHARDCHANNELS
1) "orders"
PUBSUB SHARDCHANNELS o*
1) "orders"
```
