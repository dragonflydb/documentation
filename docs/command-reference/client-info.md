---
description: Returns information about the current client connection.
---

# CLIENT INFO

## Syntax

    CLIENT INFO 

**Time complexity:** O(1)

The command returns information and statistics about the current client connection in a mostly human readable format.

The reply format is identical to that of `CLIENT LIST`, and the content consists only of information about the current client.

## Examples

```cli
CLIENT INFO
```

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): a unique string, as described at the `CLIENT LIST` page, for the current client.
