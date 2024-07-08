---
description: Learn how to use Redis PUBSUB NUMPAT to get the count of active pattern subscriptions across your Redis Pub/Sub system.
---

import PageTitle from '@site/src/components/PageTitle';

# PUBSUB NUMPAT

<PageTitle title="Redis PUBSUB NUMPAT Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

`PUBSUB NUMPAT` is a command used in Redis to get the number of patterns that are currently subscribed to by clients. This can be useful for monitoring purposes, understanding your system's usage, or debugging subscription-related issues.

## Syntax

```plaintext
PUBSUB NUMPAT
```

## Parameter Explanations

This command does not take any parameters.

## Return Values

The `PUBSUB NUMPAT` command returns an integer representing the number of patterns that are currently subscribed to by clients.

Example:

```plaintext
(integer) 5
```

## Code Examples

Using CLI:

```cli
dragonfly> PSUBSCRIBE news.*
Reading messages... (press Ctrl-C to quit)
dragonfly> PUBSUB NUMPAT
(integer) 1
dragonfly> PSUBSCRIBE sports.*
Reading messages... (press Ctrl-C to quit)
dragonfly> PUBSUB NUMPAT
(integer) 2
```

## Best Practices

- Regularly monitor the number of pattern subscriptions to understand your application's usage.
- Use this command alongside other PUBSUB commands to get comprehensive details about subscriptions.

## Common Mistakes

- Assuming `PUBSUB NUMPAT` gives the count of all subscriptions, whereas it only counts pattern-based subscriptions.

## FAQs

### What is the difference between `PUBSUB NUMPAT` and `PUBSUB NUMSUB`?

`PUBSUB NUMPAT` returns the number of active pattern subscriptions, while `PUBSUB NUMSUB` returns the number of subscribers for each specified channel.

### Can `PUBSUB NUMPAT` help detect unused patterns?

Yes, if you notice a higher number of pattern subscriptions but no corresponding activity, it might indicate unused or redundant patterns that could be optimized.
