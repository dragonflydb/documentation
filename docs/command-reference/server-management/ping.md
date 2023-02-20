---
description: Ping the server
---

# PING

## Syntax

    PING [message]

**Time complexity:** O(1)

Returns `PONG` if no argument is provided, otherwise return a copy of the
argument as a bulk.
This command is useful for:
1. Testing whether a connection is still alive.
1. Verifying the server's ability to serve data - an error is returned when this isn't the case (e.g., during load from persistence or accessing a stale replica).
1. Measuring latency.

If the client is subscribed to a channel or a pattern, it will instead return a
multi-bulk with a "pong" in the first position and an empty bulk in the second
position, unless an argument is provided in which case it returns a copy
of the argument.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings), and specifically `PONG`, when no argument is provided.

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings) the argument provided, when applicable.

## Examples

```shell
dragonfly> PING
"PONG"
dragonfly> PING "hello world"
"hello world"
```
