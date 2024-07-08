---
description: Learn how to use Redis XGROUP DELCONSUMER to remove a consumer from a consumer group.
---

import PageTitle from '@site/src/components/PageTitle';

# XGROUP DELCONSUMER

<PageTitle title="Redis XGROUP DELCONSUMER Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`XGROUP DELCONSUMER` is a Redis command used in the context of stream processing. It allows you to remove a specific consumer from a consumer group without deleting the group itself. This can be particularly useful in scenarios where consumers are dynamically added and removed, or if a consumer has completed its task and should no longer participate in processing messages.

## Syntax

```plaintext
XGROUP DELCONSUMER <stream> <groupname> <consumername>
```

## Parameter Explanations

- `<stream>`: The name of the stream from which the consumer group is associated.
- `<groupname>`: The name of the consumer group you want to modify.
- `<consumername>`: The name of the consumer to be removed from the group.

## Return Values

The command returns an integer indicating the number of pending messages owned by the deleted consumer. If the consumer does not exist, it returns `0`.

## Code Examples

```cli
dragonfly> XADD mystream * name Alice age 30
"1654329474169-0"
dragonfly> XADD mystream * name Bob age 25
"1654329485521-0"
dragonfly> XGROUP CREATE mystream mygroup $ MKSTREAM
OK
dragonfly> XREADGROUP GROUP mygroup Alice COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) "1654329474169-0"
      2) 1) "name"
         2) "Alice"
         3) "age"
         4) "30"
dragonfly> XREADGROUP GROUP mygroup Bob COUNT 1 STREAMS mystream >
1) 1) "mystream"
   2) 1) "1654329485521-0"
      2) 1) "name"
         2) "Bob"
         3) "age"
         4) "25"
dragonfly> XGROUP DELCONSUMER mystream mygroup Alice
(integer) 1
dragonfly> XINFO CONSUMERS mystream mygroup
1) 1) "name"
   2) "Bob"
   3) "pending"
   4) (integer) 1
   5) "idle"
   6) (integer) 0
```

## Best Practices

- Ensure that the consumer you intend to delete has indeed finished processing all its pending messages, or handle reassigning those messages before deletion.
- Regularly monitor the state of your streams and consumer groups using commands like `XINFO` to maintain optimal performance and resource usage.

## Common Mistakes

- Trying to delete a consumer that does not exist, which will simply return `0`.
- Not properly handling pending messages from the consumer being deleted, potentially leading to unprocessed data.

## FAQs

### What happens to the pending messages of the deleted consumer?

The pending messages need to be handled separately as they do not automatically get reassigned. You may use commands like `XPENDING` to review and manage these messages.

### Can I delete a consumer group using XGROUP DELCONSUMER?

No, `XGROUP DELCONSUMER` is only for removing individual consumers. To delete a consumer group, use `XGROUP DESTROY`.
