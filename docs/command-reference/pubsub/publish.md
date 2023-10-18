---
description:  Learn how to use Redis PUBLISH to distribute data to all subscribers of a specific channel in your messaging system.
---
import PageTitle from '@site/src/components/PageTitle';

# PUBLISH

<PageTitle title="Redis PUBLISH Command (Documentation) | Dragonfly" />

## Syntax

    PUBLISH channel message

**Time complexity:** O(N+M) where N is the number of clients subscribed to the receiving channel and M is the total number of subscribed patterns (by any client).

**ACL categories:** @pubsub, @fast

Posts a message to the given channel.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of clients that received the message. 

## Examples

```shell
user:1> PSUBSCRIBE "h[ae]llo"
user:2> PSUBSCRIBE "h*llo"
---
dragonfly> PUBLISH "hello" message1
(integer) 2 
dragonfly> PUBLISH "hllo" message2
(integer) 1 # user 2
dragonfly> PUBLISH "heello" message3
(integer) 1 # user 2
dragonfly> PUBLISH "hello world" message4
(integer) 0
```
