---
description: Learn how to use Redis SUBSCRIBE to listen for new messages published on specified channels, ideal for event-driven programming paradigms.
---

import PageTitle from '@site/src/components/PageTitle';

# SUBSCRIBE

<PageTitle title="Redis SUBSCRIBE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `SUBSCRIBE` command in Redis is used for subscribing to channels. Once a client issues this command, it will receive messages that are published to the specified channels. This is commonly used for building real-time messaging systems, chat applications, and notification services.

## Syntax

```plaintext
SUBSCRIBE channel [channel ...]
```

## Parameter Explanations

- **channel**: The name of the channel to which you want to subscribe. You can specify multiple channels separated by spaces.

## Return Values

The command returns an array where the first element is the type of message ("subscribe"), the second element is the name of the channel, and the third element is the number of channels the client is currently subscribed to.

Example:

```plaintext
1) "subscribe"
2) "mychannel"
3) (integer) 1
```

## Code Examples

```cli
dragonfly> SUBSCRIBE mychannel
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "mychannel"
3) (integer) 1
# When a message is published to 'mychannel'
1) "message"
2) "mychannel"
3) "Hello, world!"
```

## Best Practices

- Ensure your application handles reconnections gracefully as network failures can interrupt subscriptions.
- Avoid subscribing to a large number of channels from a single client, as it can impact performance.

## Common Mistakes

- Subscribing to channels without having proper handling for incoming messages, leading to data loss or unresponsive clients.
- Forgetting that once a client subscribes to channels, it can't issue other commands until it unsubscribes.

## FAQs

### How can I unsubscribe from a channel?

Use the `UNSUBSCRIBE` command with the name of the channel you wish to leave.

### Can a client subscribe to patterns of channels?

Yes, use the `PSUBSCRIBE` command to subscribe to channels matching a pattern.
