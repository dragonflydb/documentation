---
description:  Learn how to use Redis XGROUP CREATECONSUMER to create a new consumer in a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP CREATECONSUMER

<PageTitle title="Redis XGROUP CREATECONSUMER Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `XGROUP CREATECONSUMER` command is used to explicitly create a consumer within a consumer group for a stream.
This command is part of the streams data type which facilitates managing consumer groups and processing data in a distributed manner.

## Syntax

```shell
XGROUP CREATECONSUMER key groupname consumername
```

## Parameter Explanations

- `key`: The key of the stream for which the consumer is being created.
- `groupname`: The name of the consumer group within the stream.
- `consumername`: The name of the consumer to be added to the specified group.

## Return Values

- The command returns `1` if a new consumer is successfully created.
- If the consumer already exists, it returns `0`.

## Code Examples

### Basic Example

Create a new consumer in a consumer group:

```shell
# Create a stream with items
dragonfly$> XADD mystream * field1 value1
"1609471230723-0"

dragonfly$> XGROUP CREATE mystream mygroup 0
OK

# Create a consumer named 'consumer-1' in 'mygroup'.
dragonfly$> XGROUP CREATECONSUMER mystream mygroup consumer-1
(integer) 1
```

### Attempt to Create an Existing Consumer

Recreate the same consumer to demonstrate the return value:

```shell
# Attempt to create an existing consumer.
dragonfly$> XGROUP CREATECONSUMER mystream mygroup consumer-1
(integer) 0 # Consumer already exists.
```

## Best Practices

- Ensure unique consumer names within a group to prevent operational conflicts.
- Utilize consumer groups for efficient distributed data processing and to maintain a balanced load among consumers.

## Common Mistakes

- Not creating the consumer group before adding consumers, which will result in an error.
- Using the wrong `key` or `groupname`, leading to failed consumer creation attempts.

## FAQs

### What happens if the consumer group does not exist?

If the specified consumer group does not exist, `XGROUP CREATECONSUMER` will return an error. 
Ensure the group is created with `XGROUP CREATE` before adding consumers.

### Can a consumer belong to multiple groups?

Consumers are specific to the consumer group they are created within.
A consumer with the same name can exist in different groups, handling messages independently in each context.