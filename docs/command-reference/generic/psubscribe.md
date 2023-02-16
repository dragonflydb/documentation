---
description: Listen for messages published to channels matching the given patterns
---

# PSUBSCRIBE

## Syntax

    PSUBSCRIBE pattern [pattern ...]

**Time complexity:** O(N) where N is the number of patterns the client is already subscribed to.

Subscribes the client to the given patterns.

Supported glob-style patterns:

* `h?llo` subscribes to `hello`, `hallo` and `hxllo`
* `h*llo` subscribes to `hllo` and `heeeello`
* `h[ae]llo` subscribes to `hello` and `hallo,` but not `hillo`

Use `\` to escape special characters if you want to match them verbatim.
