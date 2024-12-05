---
description:  Learn how to use Redis XPENDING to list pending messages of a stream's consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XPENDING

<PageTitle title="Redis XPENDING Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XPENDING` command is used to retrieve information about pending messages in a stream consumer group.
This command is particularly useful for monitoring and managing consumer group message delivery and ensuring robust processing in streaming applications.

## Syntax

```shell
XPENDING key group [start end count] [consumer]
```

## Parameter Explanations

- `key`: The name of the stream.
- `group`: The name of the consumer group to inspect.
- `start` (optional): Start ID for the range of messages to retrieve.
- `end` (optional): End ID for the range of messages.
- `count` (optional): Maximum number of messages to return.
- `consumer` (optional): When specified, the command restricts the results to messages pending for this particular consumer.

## Return Values

The `XPENDING` command returns the number of pending messages, followed by a summary with detailed information about specified pending messages.
It includes message IDs, consumer IDs, and the time since each message was claimed.

## Code Examples

### Basic Example

Get basic pending message information:

```shell
dragonfly> XADD mystream * name John
"1657659051233-0"
dragonfly> XGROUP CREATE mystream mygroup 0
OK
dragonfly> XREADGROUP GROUP mygroup myconsumer COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1657659051233-0"
         2) 1) "name"
            2) "John"
dragonfly> XPENDING mystream mygroup
1) (integer) 1
2) "1657659051233-0"
3) "myconsumer"
4) (integer) 1231
```

### Get Pending Messages for a Specific Consumer

Retrieve pending messages for a specific consumer:

```shell
dragonfly> XPENDING mystream mygroup - + 10 myconsumer
1) 1) "1657659051233-0"
   2) "myconsumer"
   3) (integer) 1231
   4) (integer) 1
```

### Filter by Message ID Range

Get pending messages within a specific ID range:

```shell
dragonfly> XPENDING mystream mygroup "1657650000000-0" "1657659999999-0" 10
1) 1) "1657659051233-0"
   2) "myconsumer"
   3) (integer) 1231
   4) (integer) 1
```

## Best Practices

- Regularly monitor pending messages to manage unacknowledged messages effectively.
- Use `XPENDING` in coordination with other stream commands like `XCLAIM` to address stuck messages.
- Limit the number of returned messages with `count` to avoid excessive data retrieval.

## Common Mistakes

- Not specifying the `group` parameter, as it is mandatory to identify the consumer group.
- Misunderstanding `start` and `end` as time ranges instead of message ID ranges.

## FAQs

### What happens if the stream or consumer group does not exist?

If the stream or consumer group does not exist, the `XPENDING` command will return an error.

### Can `start` and `end` be specified as `-` and `+`?

Yes, the special identifiers `-` and `+` can be used to indicate the smallest and largest message IDs in the stream, respectively.