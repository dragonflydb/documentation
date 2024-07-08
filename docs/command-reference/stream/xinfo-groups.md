---
description: Learn how to use Redis XINFO GROUPS to get information about consumer groups of a stream.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO GROUPS

<PageTitle title="Redis XINFO GROUPS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XINFO GROUPS` is a command used in Redis to retrieve information about the consumer groups associated with a specific stream. This command is particularly useful for monitoring and debugging purposes, providing insights into the state and status of each consumer group.

Typical scenarios where it is used include:

- Monitoring consumer group activity and health.
- Debugging issues related to message consumption in streams.
- Auditing and gathering metrics on stream processing.

## Syntax

```plaintext
XINFO GROUPS <key>
```

## Parameter Explanations

- `<key>`: The name of the stream for which you want to get information about the consumer groups.

## Return Values

The command returns an array where each element is a dictionary with details about a consumer group. Possible fields in each group's dictionary include:

- `name`: The name of the consumer group.
- `consumers`: The number of consumers in the group.
- `pending`: The number of pending messages (messages that have been delivered but not yet acknowledged).
- `last-delivered-id`: The ID of the last entry delivered to this group.
- `entries-read`: (If available) Number of entries read by the group.
- `lag`: (If available) The number of entries that are still waiting to be delivered to at least one consumer.

Example output:

```json
1)  1) "name"
    2) "group1"
    3) "consumers"
    4) (integer) 2
    5) "pending"
    6) (integer) 5
    7) "last-delivered-id"
    8) "1526569495631-0"
2)  1) "name"
    2) "group2"
    3) "consumers"
    4) (integer) 1
    5) "pending"
    6) (integer) 0
    7) "last-delivered-id"
    8) "1526569495639-0"
```

## Code Examples

```cli
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XADD mystream * field1 value1
"1638409437348-0"
dragonfly> XADD mystream * field1 value2
"1638409441234-0"
dragonfly> XINFO GROUPS mystream
1)  1) "name"
    2) "mygroup"
    3) "consumers"
    4) (integer) 0
    5) "pending"
    6) (integer) 0
    7) "last-delivered-id"
    8) "0-0"
```

## Best Practices

- Regularly monitor your consumer groups using `XINFO GROUPS` to ensure they are functioning correctly and to identify any potential bottlenecks or issues with message processing.
- Use the information provided by `XINFO GROUPS` to balance load among consumers by adding or removing them as needed based on the pending messages and consumer count.

## Common Mistakes

- Forgetting to create a consumer group before attempting to use `XINFO GROUPS`. Ensure that you have created one using `XGROUP CREATE`.
- Not specifying the correct stream key, leading to unexpected results or errors. Double-check that the key you provide exists and is indeed a stream.

## FAQs

### What does the "pending" field in the output signify?

The "pending" field indicates the number of messages that have been delivered to consumers but have not yet been acknowledged.

### How can I reduce the lag shown by `XINFO GROUPS`?

Lag can be reduced by either increasing the number of consumers in the group or optimizing the processing logic of existing consumers so they can handle messages more quickly.

### Is there a way to track individual consumer performance within a group?

Yes, use the `XINFO CONSUMERS <stream> <group>` command to get detailed information about each consumer within a specific group.
