---
description: Learn how to use Redis XGROUP CREATECONSUMER to create a new consumer in a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP CREATECONSUMER

<PageTitle title="Redis XGROUP CREATECONSUMER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XGROUP CREATECONSUMER` command in Redis is used to create a new consumer in an existing consumer group. This command is particularly useful when dealing with Redis Streams, where consumers are part of a consumer group that processes messages from the stream. Typical use cases include scaling out message processing by adding new consumers to distribute the workload.

## Syntax

```plaintext
XGROUP CREATECONSUMER <key> <groupname> <consumername>
```

## Parameter Explanations

- **`<key>`**: The name of the stream where the consumer group exists.
- **`<groupname>`**: The name of the consumer group to which the new consumer will be added.
- **`<consumername>`**: The unique name of the consumer to be created within the consumer group.

## Return Values

The command returns an integer:

- `(integer) 1` if the consumer was successfully created.
- `(integer) 0` if the consumer already exists in the specified group.

## Code Examples

Creating a new consumer in an existing consumer group using the CLI:

```cli
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XGROUP CREATECONSUMER mystream mygroup consumer1
(integer) 1
dragonfly> XGROUP CREATECONSUMER mystream mygroup consumer1
(integer) 0
dragonfly> XINFO GROUPS mystream
1) 1) "name"
   2) "mygroup"
   3) "consumers"
   4) (integer) 1
   5) "pending"
   6) (integer) 0
   7) "last-delivered-id"
   8) "0-0"
```

## Best Practices

- Ensure the stream key and consumer group exist before creating a consumer.
- Use meaningful consumer names for easier management and debugging.

## Common Mistakes

- Attempting to create a consumer in a non-existent consumer group or stream.
- Using duplicate consumer names within the same consumer group.

## FAQs

### What happens if I try to create a consumer in a non-existent consumer group?

The command will return an error since the consumer group must exist prior to adding consumers.

### Can I create multiple consumers with the same name in different consumer groups?

Yes, consumer names need to be unique only within the same consumer group.
