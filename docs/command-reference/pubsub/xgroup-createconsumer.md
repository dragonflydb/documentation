---
description: Create a consumer in a consumer group.
---

# XGROUP CREATECONSUMER

## Syntax

    XGROUP CREATECONSUMER key group consumer

**Time complexity:** O(1)

Create a consumer named `<consumername>` in the consumer group `<groupname>` of the stream that's stored at `<key>`.

Consumers are also created automatically whenever an operation, such as `XREADGROUP`, references a consumer that doesn't exist.
This is valid for `XREADGROUP` only when there is data in the stream.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the number of created consumers (0 or 1)