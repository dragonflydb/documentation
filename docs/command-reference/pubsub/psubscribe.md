---
description:  Learn how to use Redis PSUBSCRIBE to receive messages from channels matching certain patterns, ideal for flexible message handling.
---
import PageTitle from '@site/src/components/PageTitle';

# PSUBSCRIBE

<PageTitle title="Redis PSUBSCRIBE Command (Documentation) | Dragonfly" />

## Syntax

    PSUBSCRIBE pattern [pattern ...]

**Time complexity:** O(N) where N is the number of patterns the client is already subscribed to.

**ACL categories:** @pubsub, @slow

Subscribes the client to the given patterns.

Supported glob-style patterns:

* `h?llo` subscribes to `hello`, `hallo` and `hxllo` (matches a *single* character)
* `h*llo` subscribes to `hllo`, `hallo` and `heeeello` (matches a *sequence* of characters, possibly empty)
* `h[ae]llo` subscribes to `hello` and `hallo,` but not `hillo` (matches a single character from the list)

Use `\` to escape special characters if you want to match them verbatim.

