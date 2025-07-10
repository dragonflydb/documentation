---
description:  Learn how to use Redis XINFO CONSUMERS to fetch information about a stream's consumers.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO CONSUMERS

<PageTitle title="Redis XINFO CONSUMERS Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valke, the `XINFO CONSUMERS` command is used to retrieve information about the consumers of a consumer group for a given stream.
This command is helpful for monitoring the activity of consumers connected to a specific stream and can assist in troubleshooting and performance tuning.

## Syntax

```shell
XINFO CONSUMERS key group
```

- **Time complexity:** O(1)
- **ACL categories:** @read, @stream, @slow

## Parameter Explanations

- `key`: The key of the stream.
- `group`: The name of the consumer group whose consumers' information you want to retrieve.

## Return Values

- The command returns an array of information about each consumer in the consumer group.
- Each element in the array is a dictionary with details such as the consumer name, idle time, pending message count, etc.

## Code Examples

### Retrieve Information of Consumers

Get information about consumers in a consumer group:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $ MKSTREAM
OK

dragonfly$> XADD mystream * field1 value1
"1736319841099-0"

dragonfly$> XADD mystream * field2 value2
"1736319844825-0"

# Read from the stream using consumer-1.
dragonfly$> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1736319841099-0"
         2) 1) "field1"
            2) "value1"

# Get information about consumers in the consumer group.
# The output shows the consumer name, pending message count, and idle time.
dragonfly$> XINFO CONSUMERS mystream mygroup
1) 1) "name"
   2) "consumer-1"
   3) "pending"
   4) (integer) 1
   5) "idle"
   6) (integer) 5000 # Idle time in milliseconds.

# Read from the stream using consumer-2.
dragonfly$> XREADGROUP GROUP mygroup consumer-2 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1736319844825-0"
         2) 1) "field2"
            2) "value2"

# Get information about consumers in the consumer group.
# Now there are two consumers in the group, and the output shows details for both.
dragonfly$> XINFO CONSUMERS mystream mygroup
1) 1) "name"
   2) "consumer-1"
   3) "pending"
   4) (integer) 1
   5) "idle"
   6) (integer) 50000 # Idle time in milliseconds.
2) 1) "name"
   2) "consumer-2"
   3) "pending"
   4) (integer) 1
   5) "idle"
   6) (integer) 5000 # Idle time in milliseconds.
```

## Best Practices

- Regularly monitor consumer metrics to ensure that your consumer groups are efficiently processing messages.
- Use consumer idle time to detect inactive consumers and potentially rebalance workloads.

## Common Mistakes

- Failing to create a consumer group before using `XINFO CONSUMERS` will result in an error.
- Misunderstanding the interpretation of idle time; it might lead to incorrect assumptions about consumer activity.

## FAQs

### What happens if the stream or consumer group does not exist?

If the stream or consumer group does not exist, the `XINFO CONSUMERS` command will return an error indicating that the specified key or group does not exist.

### Can I use `XINFO CONSUMERS` for streams without consumer groups?

No, the `XINFO CONSUMERS` command is specifically for use with streams that have consumer group(s) defined.
