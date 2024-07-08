---
description: Learn how to use Redis PUBSUB CHANNELS to get the list of active channels in a Pub/Sub system, seamless for data monitoring.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB CHANNELS

<PageTitle title="Redis PUBSUB CHANNELS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PUBSUB CHANNELS` command in Redis is used to list the currently active channels that match a specified pattern. This command is particularly useful in scenarios where you need to monitor or debug which channels are being used in your Pub/Sub messaging system.

## Syntax

```plaintext
PUBSUB CHANNELS [pattern]
```

## Parameter Explanations

- **pattern**: (Optional) A glob-style pattern to filter the channels. If omitted, it lists all active channels.

## Return Values

The command returns an array of strings, each representing an active channel name that matches the given pattern.

Example outputs:

- `[]`: No active channels.
- `["channel1", "channel2"]`: Active channels named "channel1" and "channel2".

## Code Examples

```cli
dragonfly> PUBLISH mychannel "Hello World!"
(integer) 0
dragonfly> PUBSUB CHANNELS
1) "mychannel"
dragonfly> PUBSUB CHANNELS my*
1) "mychannel"
dragonfly> PUBSUB CHANNELS notexisting*
(empty array)
```

## Best Practices

Utilize specific patterns when querying channels to narrow down results, especially in environments with numerous active channels, to avoid performance overhead.

## Common Mistakes

A common mistake is forgetting that the command only lists channels with one or more subscribers. Channels without subscribers won't appear in the result.

## FAQs

### Why don't I see some channels listed by PUBSUB CHANNELS?

Channels without active subscribers at the time of the query won't be listed. Ensure there are subscribers to the channels you expect to see.

### Can I use regular expressions for the pattern parameter?

No, the pattern parameter uses glob-style matching, not regular expressions. Use wildcards like `*` and `?` for matching.
