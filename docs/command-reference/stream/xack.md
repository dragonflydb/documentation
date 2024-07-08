---
description: Learn how to use Redis XACK to acknowledge the processing of a message from a stream by a consumer.
---

import PageTitle from '@site/src/components/PageTitle';

# XACK

<PageTitle title="Redis XACK Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XACK` is a Redis Stream command used to acknowledge the successful processing of one or more messages in a stream. It is typically used in scenarios involving message queues where consumers need to signal that they have processed specific messages, allowing for proper tracking and potential re-processing of unacknowledged messages.

## Syntax

```cli
XACK <key> <group> <ID> [<ID> ...]
```

## Parameter Explanations

- `<key>`: The name of the stream.
- `<group>`: The consumer group that is acknowledging the messages.
- `<ID>`: The ID of the message being acknowledged. Multiple IDs can be specified.

## Return Values

`XACK` returns the number of messages successfully acknowledged.

### Examples:

1. Acknowledging a single message:
   ```cli
   (integer) 1
   ```
2. Acknowledging multiple messages:
   ```cli
   (integer) 2
   ```

## Code Examples

```cli
dragonfly> XADD mystream * name "Alice"
"1626529532936-0"
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XREADGROUP GROUP mygroup Alice COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) 1) "1626529532936-0"
         2) 1) "name"
            2) "Alice"
dragonfly> XACK mystream mygroup 1626529532936-0
(integer) 1
```

## Best Practices

- Ensure that consumer processes are designed to reliably call `XACK` after processing a message to maintain accurate tracking.
- Consider implementing retry mechanisms for cases where `XACK` fails due to transient issues.

## Common Mistakes

- Forgetting to specify the consumer group name, which results in an error.
- Attempting to acknowledge message IDs that do not exist or belong to a different stream.

## FAQs

### What happens if I `XACK` a message that doesn't exist?

If you acknowledge a non-existent message ID, Redis will simply return `(integer) 0`, indicating no messages were acknowledged.

### Can I acknowledge messages from different streams in a single `XACK` command?

No, `XACK` operates on a single stream per command. Each `XACK` command only targets the specified stream.
