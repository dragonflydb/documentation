---
description:  Learn how to use Redis XGROUP CREATECONSUMER to create a new consumer in a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP CREATECONSUMER

<PageTitle title="Redis XGROUP CREATECONSUMER Command (Documentation) | Dragonfly" />

## Syntax

    XGROUP CREATECONSUMER key group consumer

**Time complexity:** O(1)

**ACL categories:** @write, @stream, @slow

Create a consumer in a group. *<key\>* denotes the stream
and *<group\>* is the group name in which the *<consumer\>*
is being created. Both the stream and group must already
exist in order to make the operation successful.

Consumers in a group are entities that consume data. Consumers,
unless claimed explicitly, do not share received entries.
Each consumer has their own *pending entry list* (PEL) where
they store the received entries. Consumers can either read
entries from their own PEL or from the group (entries that
are not yet read by other consumers).

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers):
the number of created consumers (0 or 1)
