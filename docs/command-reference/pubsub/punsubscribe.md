---
description: Learn using Redis PUNSUBSCRIBE to unsubscribe from specific patterns of channels, ideal for dynamic message filtering.
---

import PageTitle from '@site/src/components/PageTitle';

# PUNSUBSCRIBE

<PageTitle title="Redis PUNSUBSCRIBE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PUNSUBSCRIBE` command is used in Redis to unsubscribe the client from one or more channels that match a given pattern. It's typically employed in scenarios where clients need to stop receiving messages published to specific patterns of channels, often in real-time messaging systems or pub/sub architectures.

## Syntax

```plaintext
PUNSUBSCRIBE [pattern [pattern ...]]
```

## Parameter Explanations

- `pattern`: The pattern(s) from which the client should unsubscribe. This parameter is optional. If no pattern is given, the client will unsubscribe from all previously subscribed patterns.

## Return Values

The command returns an array of messages. Each message contains three elements:

1. Type of operation (`"punsubscribe"`).
2. The pattern from which the client is unsubscribed.
3. The count of total subscriptions (patterns + channels) the client is still subscribed to.

### Example Output

```plaintext
1) "punsubscribe"
2) "news.*"
3) (integer) 0
```

## Code Examples

```cli
dragonfly> PSUBSCRIBE news.*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "news.*"
3) (integer) 1

# In another terminal, publish a message
dragonfly> PUBLISH news.sports "Sports News"
(integer) 1

# Unsubscribe from the pattern
dragonfly> PUNSUBSCRIBE news.*
1) "punsubscribe"
2) "news.*"
3) (integer) 0
```

## Best Practices

- It is good practice to manage your subscriptions effectively to avoid unnecessary processing load on both the server and the client side.

## Common Mistakes

- Forgetting to provide the correct pattern can lead to unsuccessful unsubscriptions.
- Not accounting for the fact that unsubscribing from all patterns when no patterns are provided might not be the intended behavior.
