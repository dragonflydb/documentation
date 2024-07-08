---
description: Learn how to use Redis PUBSUB SHARDNUMSUB for a list of specific channel subscriptions for shard Pub/Sub networks.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB SHARDNUMSUB

<PageTitle title="Redis PUBSUB SHARDNUMSUB Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PUBSUB SHARDNUMSUB` command in Redis is used to get the number of subscribers (exclusive of pattern subscribers) for shard channels. This can be particularly useful for monitoring and managing the load on various shard channels, ensuring balanced distribution of messages, and debugging issues related to message delivery.

## Syntax

```plaintext
PUBSUB SHARDNUMSUB [channel-1] [channel-2] ... [channel-N]
```

## Parameter Explanations

- **[channel-1], [channel-2], ..., [channel-N]**: A list of one or more shard channel names. Each channel is a string representing the name of a shard channel whose subscriber count you want to retrieve. Providing multiple channel names returns the subscriber count for each specified channel.

## Return Values

The command returns an array where each element is a pair consisting of a channel name followed by its subscriber count.

Example output:

```plaintext
1) "shard-channel-1"
2) (integer) 3
3) "shard-channel-2"
4) (integer) 5
```

## Code Examples

```cli
dragonfly> PUBSUB SHARDNUMSUB "shard-channel-1" "shard-channel-2"
1) "shard-channel-1"
2) (integer) 3
3) "shard-channel-2"
4) (integer) 5

dragonfly> PUBSUB SHARDNUMSUB "shard-channel-3"
1) "shard-channel-3"
2) (integer) 0
```

## Best Practices

- Regularly monitor shard channel subscriber counts to ensure even distribution and load balancing among your channels.
- Combine with other `PUBSUB` commands like `PUBSUB CHANNELS` and `PUBSUB NUMSUB` for comprehensive monitoring of your Pub/Sub system.

## Common Mistakes

- Omitting channel names will result in an error. Always specify at least one channel to query.
- Assuming that `PATTERN` subscribers are included; this command only counts regular subscribers.

## FAQs

### What is the difference between `SHARDNUMSUB` and `NUMSUB`?

`SHARDNUMSUB` specifically deals with shard channels, whereas `NUMSUB` deals with normal channels.

### Can `SHARDNUMSUB` be used without specifying any channels?

No, you need to specify at least one shard channel to get the subscriber count.
