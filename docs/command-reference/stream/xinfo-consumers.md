---
description: Learn how to use Redis XINFO CONSUMERS to fetch information about a stream's consumers.
---

import PageTitle from '@site/src/components/PageTitle';

# XINFO CONSUMERS

<PageTitle title="Redis XINFO CONSUMERS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XINFO CONSUMERS` command in Redis provides information about the consumers of a specific consumer group from a stream. It is useful for monitoring and debugging purposes, such as checking the status of various consumers within a group, identifying idle consumers, and understanding each consumer's pending messages count.

## Syntax

```plaintext
XINFO CONSUMERS <key> <groupname>
```

## Parameter Explanations

- `<key>`: The name of the stream.
- `<groupname>`: The name of the consumer group whose consumers you want to inspect.

## Return Values

The command returns an array of information for each consumer in the specified consumer group. Each consumer's details are provided as key-value pairs, including:

- `name`: The name of the consumer.
- `pending`: The number of pending messages for this consumer.
- `idle`: The number of milliseconds since the consumer's last attempted interaction with the stream.

### Example Output

```plaintext
1) 1) "name"
   2) "consumer-1"
   3) "pending"
   4) (integer) 5
   5) "idle"
   6) (integer) 1748237
2) 1) "name"
   2) "consumer-2"
   3) "pending"
   4) (integer) 13
   5) "idle"
   6) (integer) 982374
```

## Code Examples

```cli
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XADD mystream * field1 value1
"1688852531964-0"
dragonfly> XADD mystream * field1 value2
"1688852532964-0"
dragonfly> XREADGROUP GROUP mygroup consumer-1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1688852531964-0"
         2) 1) "field1"
            2) "value1"
dragonfly> XREADGROUP GROUP mygroup consumer-2 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1688852532964-0"
         2) 1) "field1"
            2) "value2"
dragonfly> XINFO CONSUMERS mystream mygroup
1) 1) "name"
   2) "consumer-1"
   3) "pending"
   4) (integer) 1
   5) "idle"
   6) (integer) 15000
2) 1) "name"
   2) "consumer-2"
   3) "pending"
   4) (integer) 1
   5) "idle"
   6) (integer) 10000
```

## Best Practices

- Regularly monitor the consumers using `XINFO CONSUMERS` to identify any potential bottlenecks or idle consumers.
- Combine this command with other `XINFO` commands to get a comprehensive overview of your stream's health and activity.

## Common Mistakes

- Misunderstanding the `idle` time as message age; it actually represents the time since the consumer last interacted with the stream.
- Not specifying both the stream key and the consumer group name, which will result in an error.

## FAQs

### What does the `idle` value represent?

The `idle` value indicates the number of milliseconds that have elapsed since the consumer last attempted to read from the stream.

### How can I reset a consumer's idle time?

The idle time is reset whenever the consumer reads a message from the stream using commands like `XREADGROUP`.

### Can I use `XINFO CONSUMERS` to monitor streams other than those with consumer groups?

No, `XINFO CONSUMERS` is specifically designed to provide information about consumers within a consumer group.
