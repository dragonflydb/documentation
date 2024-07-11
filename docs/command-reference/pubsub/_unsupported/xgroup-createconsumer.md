---
description: Learn how to use Redis XGROUP CREATECONSUMER to create a new consumer in a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP CREATECONSUMER

<PageTitle title="Redis XGROUP CREATECONSUMER Command (Documentation) | Dragonfly" />

## Syntax

    XGROUP CREATECONSUMER key group consumer

**Time complexity:** O(1)

Create a consumer named `<consumername>` in the consumer group `<groupname>` of the stream that's stored at `<key>`.

Consumers are also created automatically whenever an operation, such as `XREADGROUP`, references a consumer that doesn't exist.
This is valid for `XREADGROUP` only when there is data in the stream.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of created consumers (0 or 1)
