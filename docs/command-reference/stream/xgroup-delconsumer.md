---
description:  Learn how to use Redis XGROUP DELCONSUMER to remove a consumer from a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DELCONSUMER

<PageTitle title="Redis XGROUP DELCONSUMER Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP DELCONSUMER` command is used to remove a specific consumer from a consumer group in a stream.
This is crucial for managing stream groups by allowing the removal of consumers that are no longer in use, thus ensuring the efficiency and performance of your stream processing.

## Syntax

```shell
XGROUP DELCONSUMER key groupname consumername
```

## Parameter Explanations

- `key`: The key of the stream.
- `groupname`: The name of the consumer group to which the consumer belongs.
- `consumername`: The name of the consumer to be removed from the group.

## Return Values

The command returns an integer representing the number of pending messages that were owned by the consumer and transferred to other consumers.

## Code Examples

### Basic Example

Remove a consumer from a group:

```shell
# Create a stream and a consumer group
dragonfly> XADD mystream * name "Alice"
"1530105600018-0"
dragonfly> XGROUP CREATE mystream mygroup 0
OK

# Add a consumer to the group
dragonfly> XREADGROUP GROUP mygroup consumer1 COUNT 1 STREAMS mystream 0
1) 1) "mystream"
   2) 1) 1) "1530105600018-0"
         2) 1) "name"
            2) "Alice"

# Remove the consumer from the group
dragonfly> XGROUP DELCONSUMER mystream mygroup consumer1
(integer) 1
```

### Practical Use Case

Use `XGROUP DELCONSUMER` to manage inactive consumers:

```shell
# Assuming we have multiple consumers and want to cleanup inactive ones
dragonfly> XADD mystream * event "UserLogin" user "1001"
"1530105600022-0"
dragonfly> XGROUP CREATE mystream usergroup 0
OK
dragonfly> XREADGROUP GROUP usergroup consumer1 COUNT 1 STREAMS mystream 0
# Processing is done

# Remove the inactive consumer 'consumer1'
dragonfly> XGROUP DELCONSUMER mystream usergroup consumer1
(integer) 1
```

## Best Practices

- Regularly monitor and clean up consumers that are no longer active to keep the stream group healthy.
- Before removing a consumer, make sure to process or transfer any pending messages it might own.

## Common Mistakes

- Attempting to delete a non-existent consumer, which will result in no effect but can be part of error checks.
- Removing consumers without checking or reassigning their pending messages, leading to possible message loss or processing delay.

## FAQs

### What happens if the consumer does not exist?

If the consumer does not exist, the command returns `0`, indicating no pending messages were transferred.

### Does this command delete the consumer group itself?

No, `XGROUP DELCONSUMER` only removes an individual consumer. The group remains intact until explicitly deleted with another command.