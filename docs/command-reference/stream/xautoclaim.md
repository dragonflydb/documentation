---
description: Learn how to use Redis XAUTOCLAIM to help with message recovery, claiming pending messages from other consumers.
---

import PageTitle from '@site/src/components/PageTitle';

# XAUTOCLAIM

<PageTitle title="Redis XAUTOCLAIM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `XAUTOCLAIM` command in Redis is used to transfer ownership of pending messages in a specific stream consumer group to another consumer. This is particularly useful for handling messages that have been pending for too long due to consumer failures or long processing times. Typical scenarios include recovering stuck messages and ensuring they are processed by active consumers.

## Syntax

```plaintext
XAUTOCLAIM <key> <group> <consumer> <min-idle-time> <start> [COUNT count] [JUSTID]
```

## Parameter Explanations

- **`<key>`**: The name of the stream.
- **`<group>`**: The name of the consumer group.
- **`<consumer>`**: The name of the new consumer claiming the messages.
- **`<min-idle-time>`**: The minimum idle time (in milliseconds) for messages to be eligible for claiming.
- **`<start>`**: The ID from which to start scanning for messages. Use "0" to scan from the beginning.
- **`COUNT count`**: (Optional) Limit the number of messages returned in one go.
- **`JUSTID`**: (Optional) Return only the IDs of the claimed messages without transferring ownership.

## Return Values

`XAUTOCLAIM` returns an array where the first element is the new start ID, and the second element is an array of claimed messages or their IDs if `JUSTID` is used.

Example Outputs:

- When transferring ownership:

  ```plaintext
  dragonfly> XAUTOCLAIM mystream mygroup consumer1 3600000 0 COUNT 2
  1) "0-0"
  2) 1) 1) "1623429200-0"
        2) 1) "field1"
           2) "value1"
     2) 1) "1623429300-0"
        2) 1) "field2"
           2) "value2"
  ```

- When using `JUSTID`:
  ```plaintext
  dragonfly> XAUTOCLAIM mystream mygroup consumer1 3600000 0 COUNT 2 JUSTID
  1) "0-0"
  2) 1) "1623429200-0"
     2) "1623429300-0"
  ```

## Code Examples

```cli
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XADD mystream * field1 value1
"1623429200-0"
dragonfly> XADD mystream * field2 value2
"1623429300-0"

# Simulate consumer1 reading a message
dragonfly> XREADGROUP GROUP mygroup consumer1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) "1623429200-0"
      2) 1) "field1"
         2) "value1"

# Simulate consumer2 reclaiming the message after it has been idle
dragonfly> XAUTOCLAIM mystream mygroup consumer2 3600000 0 COUNT 2
1) "0-0"
2) 1) 1) "1623429200-0"
        2) 1) "field1"
           2) "value1"
     2) 1) "1623429300-0"
        2) 1) "field2"
           2) "value2"

# Reclaiming with JUSTID
dragonfly> XAUTOCLAIM mystream mygroup consumer2 3600000 0 COUNT 2 JUSTID
1) "0-0"
2) 1) "1623429200-0"
     2) "1623429300-0"
```

## Best Practices

- Regularly monitor and reclaim idle messages to ensure efficient message processing and avoid bottlenecks.
- Use the `COUNT` option to limit the number of messages claimed per operation, preventing potential performance issues.

## Common Mistakes

- Forgetting to specify the `JUSTID` option when you don't need the full message data, which can unnecessarily increase the response size.
- Not setting the appropriate `min-idle-time`, leading to either missing eligible messages or claiming messages too early.

## FAQs

### What happens if no messages meet the idle time criteria?

If no messages meet the specified `min-idle-time`, Redis returns an empty array for the claimed messages part, but the new start ID
