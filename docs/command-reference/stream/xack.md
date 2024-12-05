---
description: Learn how to use Redis XACK to acknowledge the processing of a message from a stream by a consumer.
---

import PageTitle from '@site/src/components/PageTitle';

# XACK

<PageTitle title="Redis XACK Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XACK` command is used to acknowledge one or more messages in a stream that have been successfully processed.
This is particularly useful in stream processing systems where consumers must signal that a message has been handled, helping to manage message delivery and retention more efficiently within a consumer group.

## Syntax

```shell
XACK key group id [id ...]
```

## Parameter Explanations

- `key`: The name of the stream.
- `group`: The name of the consumer group.
- `id`: The ID of the message to acknowledge. Multiple IDs can be specified.

## Return Values

The command returns an integer indicating the number of messages that were successfully acknowledged.

## Code Examples

### Basic Acknowledgement Example

Acknowledge a single message that has been processed:

```shell
dragonfly> XADD mystream * name Alice age 30
"1609097574170-0"
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XREADGROUP GROUP mygroup Alice COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1609097574170-0"
         2) 1) "name"
            2) "Alice"
            3) "age"
            4) "30"
dragonfly> XACK mystream mygroup 1609097574170-0
(integer) 1
```

### Acknowledging Multiple Messages

Acknowledge multiple messages after processing:

```shell
dragonfly> XADD mystream * name Bob age 25
"1609097574171-0"
dragonfly> XADD mystream * name Charlie age 40
"1609097574172-0"
dragonfly> XACK mystream mygroup 1609097574171-0 1609097574172-0
(integer) 2
```

### Handling Non-existent IDs

Acknowledge attempt on a non-existent message ID:

```shell
dragonfly> XACK mystream mygroup 1609097574173-0
(integer) 0  # No acknowledgment since the ID does not exist.
```

## Best Practices

- Use `XACK` to signal message processing completion to avoid reprocessing.
- Implement proper error handling to manage message IDs that may no longer exist or are not yet acknowledged.

## Common Mistakes

- Not creating a consumer group before attempting to acknowledge messages; `XACK` requires a valid consumer group.
- Attempting to acknowledge messages using IDs that were never read by the group.

## FAQs

### What happens if the message ID is not found?

If the message ID does not exist in the pending entries list of the consumer group, `XACK` returns `0`.

### Can `XACK` be used for automatic acknowledgement?

No, `XACK` requires explicit calls to acknowledge messages after successful processing by consumers.
