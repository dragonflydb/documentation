---
description:  Learn how to use Redis XREADGROUP for consumer groups to read from streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XREADGROUP

<PageTitle title="Redis XREADGROUP Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XREADGROUP` command is used to read messages from a stream, primarily used within the context of consumer groups. 
Consumer groups in Redis allow you to implement message feed processing, where different consumers can read distinct messages avoiding reading duplicates, thus enhancing efficient data processing.

## Syntax

```shell
XREADGROUP GROUP groupname consumer [COUNT count] [BLOCK milliseconds] 
    [NOACK] STREAMS key [key ...] ID [ID ...]
```

## Parameter Explanations

- `groupname`: The name of the consumer group.
- `consumer`: The name of the consumer within the group.
- `COUNT count` (optional): Limits the number of returned entries. Default is all available entries.
- `BLOCK milliseconds` (optional): Blocks the command and waits for specified milliseconds if no entries are available.
- `NOACK` (optional): Specifies the server should not maintain the acknowledged status of the messages.
- `key`: One or more stream keys to read from.
- `ID`: One or more IDs, typically `>`, to indicate reading new messages.

## Return Values

The command returns entries from the stream, grouped by stream name. 
If no entries are available and the `BLOCK` option was not used, it returns an empty array.

## Code Examples

### Basic Example

Create a consumer group and read messages:

```shell
dragonfly$> XADD mystream * field1 value1
"16082358984-0"
dragonfly$> XGROUP CREATE mystream mygroup 0
OK
dragonfly$> XREADGROUP GROUP mygroup consumer1 STREAMS mystream >
1) "mystream"
2) 1) 1) "16082358984-0"
      2) 1) "field1"
         2) "value1"
```

### Reading Specific Number of Messages

Read up to two messages from a stream:

```shell
dragonfly$> XADD mystream * field2 value2
"16082358985-0"
dragonfly$> XADD mystream * field3 value3
"16082358986-0"
dragonfly$> XREADGROUP GROUP mygroup consumer1 COUNT 2 STREAMS mystream >
1) "mystream"
2) 1) 1) "16082358985-0"
      2) 1) "field2"
         2) "value2"
   2) 1) "16082358986-0"
      2) 1) "field3"
         2) "value3"
```

### Using `XREADGROUP` with `BLOCK`

Wait for new messages for up to 2000 milliseconds:

```shell
dragonfly$> XREADGROUP GROUP mygroup consumer2 BLOCK 2000 STREAMS mystream >
```

## Best Practices

- Use consumer groups to parallelize the processing of a stream across multiple workers.
- Consider using the `ACK` command frequently to acknowledge processed messages for memory efficiency.
- Selectively use the `BLOCK` option to avoid unnecessary database polling, especially in high-throughput systems.

## Common Mistakes

- Forgetting to create a consumer group using `XGROUP CREATE` before calling `XREADGROUP`.
- Misunderstanding blocking behavior when using the `BLOCK` option without a timeout, which can lead to hanging processes.
- Ignoring the need for message acknowledgment unless `NOACK` is specified.

## FAQs

### What happens if a stream key doesn't exist?

The `XREADGROUP` command will return an empty array if a stream key does not exist or if there are no messages to read.

### How can I include already read messages?

To re-read messages, specify the appropriate entry IDs instead of using just the `>` character in the `ID` argument.