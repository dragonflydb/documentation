---
description:  Learn how to use Redis CLIENT pause command to manage clients connected to the Redis server.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT PAUSE

<PageTitle title="Redis CLIENT PAUSE (Documentation) | Dragonfly" />

## Syntax

    CLIENT PAUSE timeout [WRITE | ALL]

**Time complexity:** O(1)
**ACL categories:** @admin, @slow, @dangerous, @connection

CLIENT PAUSE is a connections control command able to suspend all the Dragonfly clients for the specified amount of time (in milliseconds).

The command performs the following actions:

It stops processing all the pending commands from normal and pub/sub clients for the given mode. However interactions with replicas will continue normally. Note that clients are formally paused when they try to execute a command, so no work is taken on the server side for inactive clients.
However it returns `OK` to the caller as soon as possible, so the `CLIENT PAUSE` command execution is not paused by itself.
When the specified amount of time has elapsed, all the clients are unblocked: this will trigger the processing of all the commands accumulated in the query buffer of every client during the pause.
Client pause currently supports two modes:

* ALL: This is the default mode. All client commands are blocked.
* WRITE: Clients are only blocked if they attempt to execute a write command.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` or an error if the timeout is invalid.
