---
description: Learn how to use Redis XCLAIM to change the ownership of a pending message.
---

import PageTitle from '@site/src/components/PageTitle';

# XCLAIM

<PageTitle title="Redis XCLAIM Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XCLAIM` is a Redis command used in the context of streams to transfer ownership of pending messages from one consumer to another. This is particularly useful in scenarios where the original consumer may have crashed or stalled, and you need to reassign the message for processing by another consumer.

## Syntax

```cli
XCLAIM <stream> <group> <consumer> <min-idle-time> <ID> [<ID> ...] [IDLE <ms>] [TIME <mstime>] [RETRYCOUNT <count>] [FORCE] [JUSTID]
```

## Parameter Explanations

- **`stream`**: The name of the stream.
- **`group`**: The consumer group that the consumers belong to.
- **`consumer`**: The new consumer that will take ownership of the messages.
- **`min-idle-time`**: Minimum idle time (in milliseconds) that a message must have been idle before it can be claimed.
- **`ID`**: The ID of the message(s) to claim.
- **`IDLE <ms>`**: Optional. Set the idle time (in milliseconds) for the claimed messages.
- **`TIME <mstime>`**: Optional. Sets the last-delivered time in milliseconds epoch format. Useful for copying exact delivery times.
- **`RETRYCOUNT <count>`**: Optional. Updates retry counter for the claimed messages.
- **`FORCE`**: Optional. Claim messages even if they are not idle.
- **`JUSTID`**: Optional. Return only the IDs of the claimed messages, not the message bodies.

## Return Values

The `XCLAIM` command returns the claimed messages. If the `JUSTID` option is used, it returns only the IDs of the claimed messages.

Examples:

- Without `JUSTID`:
  ```cli
  dragonfly> XCLAIM mystream mygroup newconsumer 3600000 1526569495631-0
  1) 1) "1526569495631-0"
     2) 1) "field1"
        2) "value1"
        3) "field2"
        4) "value2"
  ```
- With `JUSTID`:
  ```cli
  dragonfly> XCLAIM mystream mygroup newconsumer 3600000 1526569495631-0 JUSTID
  1) "1526569495631-0"
  ```

## Code Examples

```cli
dragonfly> XADD mystream * field1 value1 field2 value2
"1526569495631-0"
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XREADGROUP GROUP mygroup consumer1 COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1526569495631-0"
         2) 1) "field1"
            2) "value1"
            3) "field2"
            4) "value2"
dragonfly> XPENDING mystream mygroup
1) "1526569495631-0"
2) (integer) 1
3) (integer) 1626569495631
4) 1) 1) "consumer1"
      2) (integer) 1
dragonfly> XCLAIM mystream mygroup consumer2 3600000 1526569495631-0
1) 1) "1526569495631-0"
   2) 1) "field1"
      2) "value1"
      3) "field2"
      4) "value2"
```

## Best Practices

- Ensure you set an appropriate `min-idle-time` to avoid claiming messages too early, which might lead to duplicate processing.
- Use the `JUSTID` option if you only need the message IDs to optimize performance, especially when dealing with large messages.

## Common Mistakes

- Setting `min-idle-time` too low, resulting in premature claiming of messages.
- Forgetting to include the necessary optional parameters (`IDLE`, `TIME`, etc.) which might be crucial for specific use cases.
- Using `FORCE` without understanding its implications, leading to potential data consistency issues.

## FAQs

### When should I use the `FORCE` option?

You should use the `FORCE` option when you need to claim messages regardless of their idle time. This can be useful in urgent scenarios but use
