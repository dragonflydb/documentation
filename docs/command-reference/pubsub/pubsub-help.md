---
description: Learn how to use Redis PUBSUB HELP to get guidance on usage details of the PUBSUB command in your Redis messaging setup.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB HELP

<PageTitle title="Redis PUBSUB HELP Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`PUBSUB HELP` is a Redis command that provides information about the available Pub/Sub (Publish/Subscribe) subcommands. This is particularly useful when you want to understand the capabilities of Redis's Pub/Sub system, which is often used for messaging between different parts of an application.

## Syntax

```plaintext
PUBSUB HELP
```

## Parameter Explanations

The `PUBSUB HELP` command does not take any parameters.

## Return Values

The command returns an array of strings, where each string is a brief description of a specific Pub/Sub subcommand and its usage.

Example output:

```plaintext
1) "PUBSUB <subcommand> [arg [arg ...]]"
2) "PUBSUB CHANNELS [<pattern>]"
3) "PUBSUB NUMPAT"
4) "PUBSUB NUMSUB [channel-1 ... channel-N]"
```

## Code Examples

```cli
dragonfly> PUBSUB HELP
1) "PUBSUB <subcommand> [arg [arg ...]]"
2) "PUBSUB CHANNELS [<pattern>]"
3) "PUBSUB NUMPAT"
4) "PUBSUB NUMSUB [channel-1 ... channel-N]"
```

## Best Practices

When using the Pub/Sub commands, ensure that your application can handle message delivery in an asynchronous manner, as Pub/Sub does not guarantee message order or delivery.

## Common Mistakes

### Assuming Message Delivery Guarantees

Pub/Sub does not guarantee that subscribers will receive all published messages. If you need guaranteed delivery, consider using a different messaging pattern or technology.

## FAQs

### What are the main subcommands of PUBSUB?

The main subcommands include:

- `CHANNELS`: Lists active channels.
- `NUMPAT`: Shows the number of subscriptions to patterns.
- `NUMSUB`: Displays the number of subscribers for specified channels.

### Can I use PUBSUB with Redis clusters?

Yes, but be aware that Pub/Sub messages are only delivered to clients connected to the same node. For cross-node messaging, additional infrastructure may be required.
