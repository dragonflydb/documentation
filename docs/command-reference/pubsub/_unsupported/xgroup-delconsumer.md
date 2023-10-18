---
description: Learn how to use Redis XGROUP DELCONSUMER to remove a consumer from a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DELCONSUMER

<PageTitle title="Redis XGROUP DELCONSUMER Command (Documentation) | Dragonfly" />

## Syntax

    XGROUP DELCONSUMER key group consumer

**Time complexity:** O(1)

The `XGROUP DELCONSUMER` command deletes a consumer from the consumer group.

Sometimes it may be useful to remove old consumers since they are no longer used.

Note, however, that any pending messages that the consumer had will become unclaimable after it was deleted.
It is strongly recommended, therefore, that any pending messages are claimed or acknowledged prior to deleting the consumer from the group.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of pending messages that the consumer had before it was deleted
