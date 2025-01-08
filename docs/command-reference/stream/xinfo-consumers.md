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
XINFO CONSUMERS key groupname
```

## Parameter Explanations

- `key`: The key of the stream.
- `groupname`: The name of the consumer group whose consumers' information you want to retrieve.

## Return Values

The command returns an array of information about each consumer in the consumer group.
Each element in the array is a dictionary with details such as the consumer name, idle time, pending message count, etc.

## Code Examples

### Retrieve Consumer Information

Get information about consumers in a consumer group:

```shell
dragonfly$> XGROUP CREATE mystream mygroup $
OK
dragonfly$> XREADGROUP GROUP mygroup Alice COUNT 1 STREAMS mystream >
(empty list or set)
dragonfly$> XINFO CONSUMERS mystream mygroup
1) 1) "name"
   2) "Alice"
   3) "pending"
   4) (integer) 0
   5) "idle"
   6) (integer) 12345
```

### Multiple Consumers

Suppose multiple consumers are part of the group:

```shell
dragonfly$> XREADGROUP GROUP mygroup Bob COUNT 1 STREAMS mystream >
(empty list or set)
dragonfly$> XINFO CONSUMERS mystream mygroup
1) 1) "name"
   2) "Alice"
   3) "pending"
   4) (integer) 0
   5) "idle"
   6) (integer) 12345
2) 1) "name"
   2) "Bob"
   3) "pending"
   4) (integer) 0
   5) "idle"
   6) (integer) 54321
```

## Best Practices

- Regularly monitor consumer activity to ensure that your consumer groups are efficiently processing messages.
- Use consumer idle time to detect inactive consumers and potentially rebalance workloads.

## Common Mistakes

- Failing to create a consumer group before using `XINFO CONSUMERS` will result in an error.
- Misunderstanding the interpretation of idle time; it might lead to incorrect assumptions about consumer activity.

## FAQs

### What happens if the stream or consumer group does not exist?

If the stream or consumer group does not exist, the `XINFO CONSUMERS` command will return an error indicating that the specified key or group does not exist.

### Can I use `XINFO CONSUMERS` for streams without consumer groups?

No, the `XINFO CONSUMERS` command is specifically for use with streams that have consumer groups defined.