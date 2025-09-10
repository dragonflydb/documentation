---
description:  Learn how to use Redis CLIENT CACHING command to control server-assisted client side caching for the connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT CACHING

<PageTitle title="CLIENT CACHING Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT CACHING <YES | NO>

**Time complexity:** O(1). Some options may introduce additional complexity.

**ACL categories:** @slow, @connection

**Important**: Only available when the [RESP3](https://github.com/redis/redis-specifications/blob/master/protocol/RESP3.md) protocol is used.

The `CLIENT CACHING` command changes tracking of keys **only for the next command executed by the connection**.

When tracking is enabled using [`CLIENT TRACKING`](./client-tracking.md), it is possible to specify `OPTIN` or `OPTOUT` options,
so that keys in read-only commands are not automatically remembered by the server to be invalidated later.

- When the client is in `OPTIN` mode, the standard behavior is to not track keys.
  The client can force tracking of the keys used in the next command by calling `CLIENT CACHING YES` before the command.
- Similarly, when the client is in `ON OPTOUT` mode, the standard behavior is to track keys.
  This behavior can be overridden for keys used in the next command by calling `CLIENT CACHING NO` before the command.

Again, the behavior change enforced by the `CLIENT CACHING` command is only applied to the next command.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` if the argument is valid.
An error is returned if RESP3 is not enabled, or the argument does not match the current tracking mode for the client.
For example, if `YES` is specified when the mode is not `OFF OPTIN`, or `NO` is specified when the mode is not `ON OPTOUT`.

## Examples

```shell
# Set RESP3, which is required by client-side caching.
dragonfly> HELLO 3

dragonfly> CLIENT TRACKING ON OPTOUT
OK
dragonfly> SET user_count 100
OK

# The next command will not be cached.
dragonfly> CLIENT CACHING NO
OK
dragonfly> GET user_count
"100"

# Change client tracking mode.
dragonfly> CLIENT TRACKING ON OPTIN
OK

# The next command will be cached.
dragonfly> CLIENT CACHING YES
OK
dragonfly> GET user_count
"100"
```
