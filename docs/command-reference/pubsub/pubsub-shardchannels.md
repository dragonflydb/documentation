---
description: Learn how to use Redis PUBSUB SHARDCHANNELS for a list of active channels across your shard network.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB SHARDCHANNELS

<PageTitle title="Redis PUBSUB SHARDCHANNELS Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PUBSUB SHARDCHANNELS` command in Redis is used to list active shard channels. Shard channels are a type of Pub/Sub channel that allows for more granular control over message distribution, typically used in scenarios requiring selective message broadcasting based on predefined shards.

## Syntax

```plaintext
PUBSUB SHARDCHANNELS [pattern]
```

## Parameter Explanations

- **pattern**: (Optional) A glob-style pattern to filter the shard channels. If provided, only the channels matching this pattern will be listed. If omitted, all active shard channels will be returned.

## Return Values

The command returns an array of strings where each string is the name of an active shard channel.

### Example Outputs

1. When no pattern is provided:
   ```plaintext
   1) "shard:channel:1"
   2) "shard:channel:2"
   ```
2. When a pattern is provided:
   ```plaintext
   1) "shard:channel:1"
   ```

## Code Examples

```cli
dragonfly> PUBSUB SHARDCHANNELS
1) "shard:channel:1"
2) "shard:channel:2"

dragonfly> PUBSUB SHARDCHANNELS shard:channel:*
1) "shard:channel:1"
2) "shard:channel:2"

dragonfly> PUBSUB SHARDCHANNELS shard:channel:1
1) "shard:channel:1"
```

## Best Practices

- Use specific patterns to avoid listing an overwhelming number of channels when working in large-scale applications.
- Regularly monitor active shard channels to ensure efficient resource utilization.

## Common Mistakes

- Not using patterns when necessary, leading to performance issues by trying to list too many channels at once.
- Assuming the command filters on exact matches rather than supporting glob-style patterns.

## FAQs

### What is a shard channel in Redis?

A shard channel allows messages to be distributed to subsets of subscribers based on predefined shards, facilitating more granular message control compared to regular Pub/Sub channels.

### Can I use multiple patterns with `PUBSUB SHARDCHANNELS`?

No, the command accepts only one pattern at a time to filter the shard channels.

### How does `PUBSUB SHARDCHANNELS` differ from `PUBSUB CHANNELS`?

`PUBSUB SHARDCHANNELS` lists only active shard channels, while `PUBSUB CHANNELS` lists all active channels, including non-shard ones.
