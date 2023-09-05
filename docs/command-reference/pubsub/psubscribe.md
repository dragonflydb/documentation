---
description: Listen for messages published to channels matching the given patterns
---

# PSUBSCRIBE

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

