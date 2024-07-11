---
description:  Learn how to use Redis UNSUBSCRIBE to stop receiving messages published on specific channels in your Pub/Sub setup.
---
import PageTitle from '@site/src/components/PageTitle';

# UNSUBSCRIBE

<PageTitle title="Redis UNSUBSCRIBE Command (Documentation) | Dragonfly" />

## Syntax

    UNSUBSCRIBE [channel [channel ...]]

**Time complexity:** O(N) where N is the number of clients already subscribed to a channel.

**ACL categories:** @pubsub, @slow

Unsubscribes the client from the given channels, or from all of them if none is
given.

When no channels are specified, the client is unsubscribed from all the
previously subscribed channels.
In this case, a message for every unsubscribed channel will be sent to the
client.

## Examples

```shell
user:1> SUBSCRIBE foo bar quax
---
dragonfly> PUBLISH foo message
dragonfly> PUBLISH bar message
---
user:1>
recieved 'message' in foor 
recieved 'message' in bar 
user:1> UNSUBSCRIBE
<user:1 will not recieve any more messages>
```

