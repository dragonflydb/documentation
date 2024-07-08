---
description: Learn how to use Redis XREADGROUP for consumer groups to read from streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XREADGROUP

<PageTitle title="Redis XREADGROUP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XREADGROUP` is a Redis command used to read messages from a stream for a specific consumer group. This command helps manage and distribute the processing of stream messages among multiple consumers, ensuring that each message is processed by only one consumer in the group. Typical use cases include task queues, real-time analytics, and event sourcing where reliable message consumption and processing are critical.

## Syntax

```plaintext
XREADGROUP GROUP <group> <consumer> [COUNT <count>] [BLOCK <milliseconds>] STREAMS key [key ...] ID [ID ...]
```

## Parameter Explanations

- `GROUP <group> <consumer>`: Specifies the consumer group and the consumer within that group.
- `COUNT <count>` (optional): Maximum number of elements to return. If not specified, defaults to unlimited.
- `BLOCK <milliseconds>` (optional): Time in milliseconds to block if no messages are available. Default is to return immediately.
- `STREAMS key [key ...]`: One or more stream keys to read from.
- `ID [ID ...]`: IDs to start reading from. Typically `$` (for new messages) or `0` (to read everything).

## Return Values

The command returns an array where each element represents a stream. Each stream element contains the stream name, followed by an array of messages with their IDs and fields/values pairs.

Example output:

```plaintext
1) 1) "mystream"
   2) 1) 1) "1609459200000-0"
         2) 1) "field1"
            2) "value1"
      2) 1) "1609459200001-0"
         2) 1) "field2"
            2) "value2"
```

## Code Examples

```cli
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XADD mystream * field1 value1
"1609459200000-0"
dragonfly> XADD mystream * field2 value2
"1609459200001-0"
dragonfly> XREADGROUP GROUP mygroup Alice COUNT 2 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1609459200000-0"
         2) 1) "field1"
            2) "value1"
      2) 1) "1609459200001-0"
         2) 1) "field2"
            2) "value2"
dragonfly> XACK mystream mygroup 1609459200000-0 1609459200001-0
(integer) 2
```

## Best Practices

- Use the `BLOCK` option to avoid busy-waiting for new messages. This reduces resource usage and improves efficiency.
- Always acknowledge (`XACK`) processed messages to keep the pending entries list manageable and ensure accurate tracking.

## Common Mistakes

- Forgetting to acknowledge processed messages can lead to memory bloat and inaccurate tracking of pending messages.
- Using inappropriate start IDs (e.g., using `0` instead of `$` for new messages) can result in reading already processed messages.

## FAQs

### What happens if a consumer fails to acknowledge a message?

If a consumer dies without acknowledging a message, it remains in the pending entries list and can be reassigned to another consumer using commands like `XCLAIM`.

### Can I read from multiple streams with `XREADGROUP`?

Yes, you can specify multiple stream keys after the `STREAMS` keyword, followed by the respective IDs.
