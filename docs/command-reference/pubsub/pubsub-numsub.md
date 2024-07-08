---
description: Learn how to use Redis PUBSUB NUMSUB to get a count of subscriptions for specific channels in your Pub/Sub system.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB NUMSUB

<PageTitle title="Redis PUBSUB NUMSUB Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PUBSUB NUMSUB` command in Redis is used to check the number of subscribers for a given set of channels. This can be particularly useful for monitoring purposes, allowing you to gauge the popularity or activity level of various channels within your application.

## Syntax

```plaintext
PUBSUB NUMSUB [channel-1] [channel-2] ... [channel-N]
```

## Parameter Explanations

- `channel-1`, `channel-2`, ..., `channel-N`: One or more channel names for which you want to retrieve the number of subscribers. These are optional, but at least one should be provided to get meaningful results.

## Return Values

The command returns an array. Each pair in the array consists of:

1. The channel name.
2. The number of subscribers currently subscribed to that channel.

### Example Output

```plaintext
1) "channel-1"
2) (integer) 10
3) "channel-2"
4) (integer) 20
```

## Code Examples

### Using CLI

```cli
dragonfly> SUBSCRIBE mychannel
Reading messages... (press Ctrl-C to quit)
dragonfly> PUBLISH mychannel "hello"
(integer) 1

In another terminal:

dragonfly> PUBSUB NUMSUB mychannel otherchannel
1) "mychannel"
2) (integer) 1
3) "otherchannel"
4) (integer) 0
```

## Best Practices

- Regularly monitor the subscriber count for critical channels to ensure your messaging infrastructure is functioning correctly.
- Use this command in combination with other PUBSUB commands like `PUBSUB CHANNELS` and `PUBSUB NUMPAT` to get a comprehensive view of your Pub/Sub system's status.

## Common Mistakes

- Not specifying any channels when using the command will lead to no meaningful information being returned. Always specify at least one channel to get the number of subscribers.
- Misunderstanding the output structure: Remember that the result pairs each channel name with its subscriber count.

## FAQs

### What happens if I use `PUBSUB NUMSUB` without any channels?

If you don't provide any channels, the command will not return any useful information about subscribers.

### Does `PUBSUB NUMSUB` include pattern subscriptions?

No, `PUBSUB NUMSUB` only includes direct channel subscriptions. For pattern subscription counts, use `PUBSUB NUMPAT`.
