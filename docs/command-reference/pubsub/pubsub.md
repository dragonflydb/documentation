---
description: Learn how to use Redis PUBSUB to inspect the state of the Pub/Sub subsystem, perfect for monitoring your messaging infrastructure.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB

<PageTitle title="Redis PUBSUB Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PUBSUB` command in Redis is used for managing and monitoring the publish/subscribe messaging paradigm. It allows clients to subscribe to channels, receive messages on those channels, and check the state of subscriptions. Typical use cases include real-time messaging systems, notifications, and broadcasting updates across distributed systems.

## Syntax

```plaintext
PUBSUB subcommand [argument [argument ...]]
```

## Parameter Explanations

- `subcommand`: Specifies the PUBSUB operation to perform. Can be one of:
  - `CHANNELS [pattern]`: Lists currently active channels optionally matching a pattern.
  - `NUMSUB [channel-1 channel-2 ...]`: Returns the number of subscribers for the specified channels.
  - `NUMPAT`: Returns the number of subscriptions to patterns (that is, subscriptions created using PSUBSCRIBE).

## Return Values

- `CHANNELS`: An array of active channels matching the optional pattern.
- `NUMSUB`: An array where each pair represents a channel and its subscriber count.
- `NUMPAT`: An integer representing the total number of pattern subscriptions.

## Code Examples

```cli
dragonfly> PUBSUB CHANNELS
1) "channel1"
2) "channel2"

dragonfly> PUBSUB CHANNELS ch*
1) "channel1"

dragonfly> PUBSUB NUMSUB channel1 channel2
1) "channel1"
2) (integer) 3
3) "channel2"
4) (integer) 0

dragonfly> PUBSUB NUMPAT
(integer) 2
```

## Best Practices

- Be cautious when using the `CHANNELS` subcommand in a production environment with many active channels, as this may have performance implications.

## Common Mistakes

- Forgetting to specify the subcommand when using `PUBSUB`, which results in a syntax error.
- Using incorrect patterns in `CHANNELS` can lead to unexpected results or an empty list.

## FAQs

### What happens if I subscribe to a non-existent channel?

Subscribing to a non-existent channel will not return an error. The subscription will be established, and you will start receiving messages if they are published to that channel in the future.

### How can I unsubscribe from a channel?

You can use the `UNSUBSCRIBE` command followed by the channel name(s) you wish to unsubscribe from.
