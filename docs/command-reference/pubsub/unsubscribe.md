---
description: Learn how to use Redis UNSUBSCRIBE to stop receiving messages published on specific channels in your Pub/Sub setup.
---

import PageTitle from '@site/src/components/PageTitle';

# UNSUBSCRIBE

<PageTitle title="Redis UNSUBSCRIBE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `UNSUBSCRIBE` command in Redis is used to unsubscribe the client from one or more channels that it is currently subscribed to. This command is pivotal in managing subscriptions, particularly for applications that use Redis's Pub/Sub messaging system. Typical scenarios include dynamically adjusting channel subscriptions based on application state or user preferences.

## Syntax

```
UNSUBSCRIBE [channel [channel ...]]
```

## Parameter Explanations

- `channel`: (Optional) The name of the channel to unsubscribe from. Multiple channel names can be specified, separated by spaces. If no channel is specified, the client will unsubscribe from all channels it is currently subscribed to.

## Return Values

The `UNSUBSCRIBE` command returns an array containing three elements for each channel it unsubscribes from:

1. The string "unsubscribe".
2. The name of the channel that was unsubscribed.
3. The number of channels the client is still subscribed to.

### Example Outputs

- When unsubscribing from a specific channel:
  ```
  "unsubscribe", "mychannel", 0
  ```
- When unsubscribing from all channels:
  ```
  "unsubscribe", "mychannel1", 1
  "unsubscribe", "mychannel2", 0
  ```

## Code Examples

```cli
dragonfly> SUBSCRIBE mychannel
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "mychannel"
3) (integer) 1

dragonfly> UNSUBSCRIBE mychannel
1) "unsubscribe"
2) "mychannel"
3) (integer) 0

dragonfly> SUBSCRIBE mychannel1 mychannel2
Reading messages... (press Ctrl-C to quit)
1) "subscribe"
2) "mychannel1"
3) (integer) 1
1) "subscribe"
2) "mychannel2"
3) (integer) 2

dragonfly> UNSUBSCRIBE
1) "unsubscribe"
2) "mychannel1"
3) (integer) 1
1) "unsubscribe"
2) "mychannel2"
3) (integer) 0
```

## Best Practices

- Ensure proper handling of the return values in your application logic to maintain synchronization between the client and server states.
- Consider using pattern-based subscriptions (`PSUBSCRIBE`) if your application requires listening to channels with similar naming conventions.

## Common Mistakes

- Forgetting to handle the response correctly can lead to desynchronization in the application's subscription logic.
- Assuming `UNSUBSCRIBE` without parameters only affects specific channels rather than all.

## FAQs

### What happens if I use UNSUBSCRIBE without any parameters?

Using `UNSUBSCRIBE` without any parameters will unsubscribe the client from all channels it is currently subscribed to.

### Can I use UNSUBSCRIBE within a transaction?

No, `UNSUBSCRIBE` cannot be used within a transaction (i.e., inside a `MULTI`/`EXEC` block).
