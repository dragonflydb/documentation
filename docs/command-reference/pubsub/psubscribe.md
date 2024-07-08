---
description: Learn how to use Redis PSUBSCRIBE to receive messages from channels matching certain patterns, ideal for flexible message handling.
---

import PageTitle from '@site/src/components/PageTitle';

# PSUBSCRIBE

<PageTitle title="Redis PSUBSCRIBE Explained (Better Than Official Docs)" />

## Introduction and Use Case(s)

The `PSUBSCRIBE` command in Redis is used to subscribe to channels using pattern matching. It's particularly useful for real-time applications where you need to listen to multiple channels that follow a naming convention. Common scenarios include chat applications, live notifications, and monitoring systems where messages are broadcasted on various channels.

## Syntax

```plaintext
PSUBSCRIBE pattern [pattern ...]
```

## Parameter Explanations

- `pattern`: A string pattern to match against channel names. Patterns can include special characters like `*` which matches any sequence of characters.
- `[pattern ...]`: Optional additional patterns to subscribe to multiple patterns at once.

## Return Values

Upon issuing the `PSUBSCRIBE` command, it returns a confirmation in the format:

```plaintext
1) "psubscribe"
2) "pattern"
3) (integer) number_of_subscribed_channels
```

When a message is published to a matching channel, the client receives a message in the following format:

```plaintext
1) "pmessage"
2) "pattern"
3) "channel"
4) "message"
```

## Code Examples

```cli
dragonfly> PSUBSCRIBE news.*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "news.*"
3) (integer) 1

# In another client, publish a message
dragonfly> PUBLISH news.sports "Breaking News!"
(integer) 1

# Back in the subscribing client
1) "pmessage"
2) "news.*"
3) "news.sports"
4) "Breaking News!"
```

If you subscribe to additional patterns:

```cli
dragonfly> PSUBSCRIBE updates.*, logs.*
Reading messages... (press Ctrl-C to quit)
1) "psubscribe"
2) "updates.*"
3) (integer) 2
1) "psubscribe"
2) "logs.*"
3) (integer) 3

# Publish a message to match one of the new patterns
dragonfly> PUBLISH logs.error "An error occurred."
(integer) 1

# Subscriber receives the message
1) "pmessage"
2) "logs.*"
3) "logs.error"
4) "An error occurred."
```

## Best Practices

- Combine `PSUBSCRIBE` with `PUBLISH` efficiently by keeping channel patterns simple and predictable.
- Use pattern subscriptions judiciously to avoid performance overhead from too many pattern matches.

## Common Mistakes

- Subscribing to overly broad patterns which might lead to receiving an excess of unwanted messages.
- Forgetting to handle the case when no messages are received, leading to potential blocking of the client.

## FAQs

### Can I use `PSUBSCRIBE` with other commands?

No, once a client has issued a `PSUBSCRIBE` command, it enters a mode where it can't issue other commands until it unsubscribes.

### How do I unsubscribe from a pattern?

You can use the `PUNSUBSCRIBE` command followed by the pattern you want to unsubscribe from.

```cli
dragonfly> PUNSUBSCRIBE news.*
```
