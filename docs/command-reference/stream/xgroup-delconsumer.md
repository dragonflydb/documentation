---
description:  Learn how to use Redis XGROUP DELCONSUMER to remove a consumer from a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DELCONSUMER

<PageTitle title="Redis XGROUP DELCONSUMER Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP DELCONSUMER` command is used to remove a specific consumer from a consumer group in a stream.
This is crucial for managing stream groups by allowing the removal of consumers that are no longer in use.
**Note that, deleting a consumer makes its pending messages unclaimable.**
Therefore, be sure to claim or acknowledge any pending messages before removing the consumer from the group.

## Syntax

```shell
XGROUP DELCONSUMER key group consumer
```

- **Time complexity:** O(1)
- **ACL categories:** @write, @stream, @slow

## Parameter Explanations

- `key`: The key of the stream.
- `group`: The name of the consumer group to which the consumer belongs.
- `consumer`: The name of the consumer to be removed from the group.

## Return Values

- An integer representing the number of pending messages that the consumer had before it was deleted.

## Code Examples

### Basic Example

Remove a consumer from a group:

```shell
# Create a stream.
dragonfly$> XADD mystream * name "Alice"
"1530105600018-0"

# Create a consumer group.
dragonfly$> XGROUP CREATE mystream mygroup 0
OK

# Add a consumer to the group.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1530105600018-0"
         2) 1) "name"
            2) "Alice"

# Acknowledge the message.
dragonfly$> XACK mystream mygroup "1530105600018-0"
(integer) 1

# Remove the consumer from the group.
# Since the consumer has no pending messages (acknowledged), the return value is 0.
dragonfly$> XGROUP DELCONSUMER mystream mygroup consumer-1
(integer) 0
```

## Best Practices

- Regularly monitor and clean up consumers that are no longer active to keep the consumer group healthy.
- Before removing a consumer, make sure to process and acknowledge all its pending messages,
  or have another consumer claim its pending messages.

## Common Mistakes

- Attempting to delete a non-existent consumer, which will result in no effect but can be part of error checks.
- Removing consumers without acknowledging or reassigning their pending messages, leading to possible message loss.

## FAQs

### What happens if the consumer does not exist?

If the consumer does not exist, the command returns `0`, indicating no pending messages were associated with the consumer.

### Does this command delete the consumer group itself?

No, `XGROUP DELCONSUMER` only removes an individual consumer. The consumer group remains intact until explicitly deleted with the [`XGROUP DESTROY`](xgroup-destroy.md) command.
