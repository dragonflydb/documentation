---
description: Learn how to use Redis XPENDING to list pending messages of a stream's consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XPENDING

<PageTitle title="Redis XPENDING Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XPENDING` command in Redis is used to retrieve information about pending messages in a stream's consumer group. It is particularly useful for monitoring message processing and identifying unacknowledged messages within the stream, which can be critical for debugging and ensuring reliable message delivery.

## Syntax

```cli
XPENDING key group [start end count] [consumer]
```

## Parameter Explanations

- **key**: The name of the stream.
- **group**: The name of the consumer group.
- **start** (optional): The lower bound ID for pending messages. Use '-' to start from the earliest message.
- **end** (optional): The upper bound ID for pending messages. Use '+' to end at the latest message.
- **count** (optional): Limits the number of pending messages returned.
- **consumer** (optional): Filters pending messages by a specific consumer.

## Return Values

The `XPENDING` command returns different outputs depending on its usage:

1. Without additional arguments:

   ```cli
   dragonfly> XPENDING mystream mygroup
   1) (integer) total_pending
   2) smallest_pending_id
   3) largest_pending_id
   4) 1) 1) "consumer1"
          2) (integer) pending_count_for_consumer1
      2) 1) "consumer2"
          2) (integer) pending_count_for_consumer2
   ```

2. With `start`, `end`, `count`, and optionally `consumer`:
   ```cli
   dragonfly> XPENDING mystream mygroup - + 10
   1) 1) message_id
      2) consumer
      3) milliseconds_since_delivered
      4) delivery_count
   ```

## Code Examples

```cli
dragonfly> XADD mystream * name John
"1627815448523-0"
dragonfly> XGROUP CREATE mystream mygroup 0
OK
dragonfly> XREADGROUP GROUP mygroup consumer1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) "1627815448523-0"
      2) 1) "name"
         2) "John"
dragonfly> XPENDING mystream mygroup
1) (integer) 1
2) "1627815448523-0"
3) "1627815448523-0"
4) 1) 1) "consumer1"
      2) (integer) 1
dragonfly> XPENDING mystream mygroup - + 10
1) 1) "1627815448523-0"
   2) "consumer1"
   3) (integer) 12345
   4) (integer) 1
```

## Best Practices

- Regularly monitor the pending entries list (PEL) using `XPENDING` to ensure no messages remain unacknowledged for too long, which could indicate issues with consumers or message processing.

## Common Mistakes

- Failing to properly handle unacknowledged messages can lead to data loss or inconsistencies. Always ensure that your application logic includes robust error handling and retry mechanisms for message processing.

## FAQs

### What happens if I don't specify any range or consumer?

Without specifying `start`, `end`, `count`, or `consumer`, `XPENDING` provides an overview of all pending messages in the consumer group, including the total count and information per consumer.

### Can I use `XPENDING` to get details of specific pending messages?

Yes, by providing `start`, `end`, and `count` parameters, you can retrieve details of specific pending messages, and filter further using the `consumer` parameter if needed.
