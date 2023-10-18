---
description:  Learn how to use Redis PUBSUB NUMPAT to get the count of active pattern subscriptions across your Redis Pub/Sub system.
---
import PageTitle from '@site/src/components/PageTitle';

# PUBSUB NUMPAT

<PageTitle title="Redis PUBSUB NUMPAT Command (Documentation) | Dragonfly" />

## Syntax

    PUBSUB NUMPAT 

**Time complexity:** O(1)

**ACL categories:** @pubsub, @slow

Returns the number of unique patterns that are subscribed to by clients (that are performed using the `PSUBSCRIBE` command).

Note that this isn't the count of clients subscribed to patterns, but the total number of unique patterns all the clients are subscribed to.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of patterns all the clients are subscribed to.
