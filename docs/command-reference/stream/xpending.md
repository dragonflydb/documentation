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

- **Time complexity:** O(N) with N being the number of elements returned, so asking for a small fixed number of entries per call is O(1).
  O(M), where M is the total number of entries scanned when used with the `IDLE` filter.
  When the command returns just the summary and the list of consumers is small, it runs in O(1) time.
  Otherwise, an additional O(N) time for iterating every consumer.
- **ACL categories:** @read, @stream, @slow

## Parameter Explanations

- `key`: The name of the stream.
- `group`: The name of the consumer group to inspect.
- `start` (optional): Start ID for the range of messages to retrieve.
- `end` (optional): End ID for the range of messages.
- `count` (optional): Maximum number of messages to return.
- `consumer` (optional): When specified, the command restricts the results to messages pending for this particular consumer.

## Return Values

- The `XPENDING` command returns the number of pending messages, followed by a summary with detailed information about specified pending messages.
- It includes smallest and greatest ID among the pending messages, and then list every consumer in the consumer group with at least one pending message, and the number of pending messages it has.

## Code Examples

### Basic Example

Get basic pending message information:

```shell
dragonfly$> > XADD mystream * name John
"1752095746463-0"

dragonfly$> XGROUP CREATE mystream mygroup 0
OK

dragonfly$> XREADGROUP GROUP mygroup myconsumer COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1752095746463-0"
         2) 1) "name"
            2) "John"

dragonfly$> XPENDING mystream mygroup
1) (integer) 1
2) "1752095746463-0"
3) "1752095746463-0"
4) 1) 1) "myconsumer"
      2) (integer) 1
```

### Extended Form for `XPENDING`

In order to see all the pending messages with more associated information we need to also pass a range of IDs, in a similar way we do it with [`XRANGE`](xrange.md):

```shell
dragonfly$> XPENDING mystream mygroup - + 10
1) 1) "1752095746463-0"
   2) "myconsumer"
   3) (integer) 638625
   4) (integer) 1
```

In the extended form we no longer see the summary information, instead there is detailed information for each message in the pending entries list. For each message four attributes are returned:

- The ID of the message.
- The name of the consumer (the current owner) that fetched the message and has still to acknowledge it.
- The number of milliseconds that elapsed since the last time this message was delivered to this consumer.
- The number of times this message was delivered.

It is also possible to pass an additional argument, the consumer, in order to see the messages having a specific owner:

```shell
dragonfly$> XPENDING mystream mygroup - + 10 myconsumer
```

### Filter by Idle Time

It is also possible to filter pending stream entries by their idle-time, given in milliseconds:

```shell
dragonfly$> XPENDING mystream mygroup IDLE 10000 - + 10
1) 1) "1752095746463-0"
   2) "myconsumer"
   3) (integer) 997525
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
