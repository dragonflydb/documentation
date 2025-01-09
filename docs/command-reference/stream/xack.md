---
description: Learn how to use Redis XACK to acknowledge the processing of a message from a stream by a consumer.
---

import PageTitle from '@site/src/components/PageTitle';

# XACK

<PageTitle title="Redis XACK Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XACK` command is used to acknowledge one or more messages in a stream that have been successfully processed.
It is useful in stream processing systems where consumers must signal that a message has been handled, helping to manage message delivery and retention more efficiently within a consumer group.
After successfully processing a message, a consumer should call `XACK` to prevent reprocessing and remove the message from the Pending Entries List (PEL).

## Syntax

```shell
XACK key group id [id ...]
```

## Parameter Explanations

- `key`: The name of the stream.
- `group`: The name of the consumer group.
- `id`: The ID of the message to acknowledge. Multiple IDs can be specified.

## Return Values

- The command returns an integer indicating the number of messages that were successfully acknowledged.
- Message IDs that are no longer be part of the PEL (i.e., already been acknowledged) will not be considered successful acknowledgments.
- If the stream or the consumer group does not exist, the command is a no-op and returns `0`.

## Code Examples

### Basic Acknowledgement Example

Acknowledge a single message that has been processed:

```shell
dragonfly$> XADD mystream * name Alice age 20
"1609097574170-0"

dragonfly$> XGROUP CREATE mystream mygroup 0 MKSTREAM
OK

dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1609097574170-0"
         2) 1) "name"
            2) "Alice"
            3) "age"
            4) "20"

dragonfly$> XACK mystream mygroup "1609097574170-0"
(integer) 1
```

### Acknowledging Multiple Messages

Acknowledge multiple messages after processing:

```shell
dragonfly$> XADD mystream * name Bob age 25
"1609097574171-0"

dragonfly$> XADD mystream * name Charlie age 30
"1609097574172-0"

# The consumer reads the 2 new messages.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 2 STREAMS mystream >
# ...

# Acknowledge the 2 messages for the consumer group.
dragonfly$> XACK mystream mygroup "1609097574171-0" "1609097574172-0"
(integer) 2
```

### Handling Non-existent IDs

Acknowledge attempt on a non-existent message ID:

```shell
dragonfly$> XACK mystream mygroup "1609097574173-0"
(integer) 0  # No acknowledgment since the ID does not exist.
```

## Best Practices

- Use `XACK` to signal message processing completion to avoid reprocessing and free up resources.
- Implement proper error handling to manage message IDs that may no longer exist or are not yet acknowledged.

## Common Mistakes

- Attempting to acknowledge messages using IDs that were never read by the group.

## FAQs

### What happens if the message ID is not found?

If the message ID does not exist in the pending entries list of the consumer group, `XACK` returns `0`.

### Can `XACK` be used for automatic acknowledgement?

No, `XACK` requires explicit calls to acknowledge messages after successful processing by consumers.
