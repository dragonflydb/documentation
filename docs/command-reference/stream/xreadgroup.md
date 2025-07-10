---
description:  Learn how to use Redis XREADGROUP for consumer groups to read from streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XREADGROUP

<PageTitle title="Redis XREADGROUP Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XREADGROUP` command is used to read messages from a stream, primarily used within the context of consumer groups. 
Consumer groups allow you to implement fan-out message processing, where different consumers can read distinct messages avoiding reading duplicates, thus enhancing efficient data processing.

## Syntax

```shell
XREADGROUP GROUP groupname consumer [COUNT count] [BLOCK milliseconds] 
    [NOACK] STREAMS key [key ...] id [id ...]
```

## Parameter Explanations

- `GROUP groupname`: The name of the consumer group.
- `consumer`: The name of the consumer within the group.
- `COUNT count` (optional): Limits the number of returned entries. Default is all available entries.
- `BLOCK milliseconds` (optional): Blocks the command and waits for specified milliseconds if no entries are available.
- `NOACK` (optional): Can be used to avoid adding the message to the pending entries list (PEL) in cases where strong reliability is not a requirement and the occasional message loss is acceptable. This is equivalent to acknowledging the message when it is read.
- `key`: One or more stream keys to read from.
- `id`: One or more IDs, typically `>`, to indicate reading new messages.

Once a consumer successfully processes a message, it should call `XACK` so that such message does not get processed again, and as a side effect, the PEL entry about this message is also purged, releasing memory from the Dragonfly server.

## Return Values

- The command returns entries from the stream for a consumer, grouped by stream name. 
- If the `BLOCK` option is used and a timeout occurs, or if there is no stream that can be served, `nil` is returned.

## Code Examples

### Basic Example

Create a consumer group and read messages:

```shell
dragonfly$> XADD mystream * field1 value1
"16082358984-0"

dragonfly$> XGROUP CREATE mystream mygroup 0
OK

dragonfly$> XREADGROUP GROUP mygroup myconsumer STREAMS mystream >
1) "mystream"
2) 1) 1) "16082358984-0"
      2) 1) "field1"
         2) "value1"
```

### Reading Specific Number of Messages

Read up to two messages from a stream:

```shell
dragonfly$> XADD mystream * field1 value1
"1752103450737-0"

dragonfly$> XADD mystream * field2 value2
"1752103459160-0"

dragonfly$> XADD mystream * field3 value3
"1752103462157-0"

dragonfly$> XGROUP CREATE mystream mygroup 0
OK

dragonfly$> XREADGROUP GROUP mygroup myconsumer COUNT 2 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1752103450737-0"
         2) 1) "field1"
            2) "value1"
      2) 1) "1752103459160-0"
         2) 1) "field2"
            2) "value2"
```

### Using `XREADGROUP` with `BLOCK`

Wait for new messages for up to 2000 milliseconds:

```shell
dragonfly$> XREADGROUP GROUP mygroup myconsumer BLOCK 2000 STREAMS mystream >
```

## Best Practices

- Use consumer groups to parallelize the processing of a stream across multiple consumer workers.
- Consider using the `XACK` command frequently to acknowledge processed messages for memory efficiency.
- Selectively use the `BLOCK` option to avoid unnecessary polling.

## Common Mistakes

- Forgetting to create a consumer group using `XGROUP CREATE` before calling `XREADGROUP`.
- Using the `BLOCK` option without a reasonable timeout, which can lead to hanging processes.
- Ignoring the need for message acknowledgment unless `NOACK` is specified.

## FAQs

### What happens if the stream or consumer group does not exist?

If the stream or consumer group does not exist, the `XREADGROUP` command will return an error.

### How can I include already read messages?

To reread messages, specify the appropriate entry IDs instead of using just the `>` character as the `id` argument.
Note that a consumer group **can only reread unacknowledged messages from the same group**.
