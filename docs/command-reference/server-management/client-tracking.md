---
description:  Learn how to use Redis CLIENT TRACKING command to control server-assisted client side caching for the connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT TRACKING

<PageTitle title="CLIENT TRACKING Command (Documentation) | Dragonfly" />

## Syntax

```
CLIENT TRACKING <ON | OFF> [OPTIN] [OPTOUT] [NOLOOP]
```

**Time complexity:** O(1). Some options may introduce additional complexity.

**ACL categories:** @slow, @connection

**Important**: New in Dragonfly v1.14, only available when the [RESP3](https://github.com/redis/redis-specifications/blob/master/protocol/RESP3.md) protocol is used.

The `CLIENT TRACKING` command enables the tracking feature of the Dragonfly server, which is used for server-assisted client side caching.
See more details about server-assisted client side caching in the [Redis documentation](https://redis.io/docs/latest/develop/use/client-side-caching/).

When tracking is enabled, Dragonfly remembers the keys that the connection requested in order to send later invalidation messages when such keys are modified.
Invalidation messages are sent in the same connection when the RESP3 protocol is used.
It is very important to note that **only when the client reads a key after enabling tracking will Dragonfly start tracking that key**.
Solely creating a key will not make Dragonfly track the key. See the examples below for more details.

The feature will remain active in the current connection for all its life, unless tracking is disabled with `CLIENT TRACKING OFF` at some point,
and Dragonfly stops tracking the keys for the connection, and no invalidation messages are sent.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): `OK` if the connection was
successfully put in tracking mode or if the tracking mode was successfully disabled. Otherwise, an error is returned.

## Options

`OPTIN`: Do not track keys for read only commands unless they are called immediately after a `CLIENT CACHING YES` command.

`OPTOUT`: Track keys in read only commands unless they are called immediately after a `CLIENT CACHING NO` command.

`NOLOOP`: Do not send notifications for keys modified by the current connection itself.

## Examples

Use two clients to connect to the Dragonfly server using the RESP3 protocol.
Switching to the RESP3 protocol can be done with the [`HELLO`](./hello.md) command.
Alternatively, clients or SDKs may have a configuration option to use the RESP3 protocol (i.e., `redis-cli -3`) upon connection.

In the example below, `client-1` is put in tracking mode.
Note that creating a non-existing key will not make Dragonfly track the key.
Instead, the key must be read after tracking is enabled to start being tracked.

```shell
### client-1 ###

# Switch protocol to RESP3, output omitted.
dragonfly> HELLO 3

# Switch on client tracking.
dragonfly> CLIENT TRACKING ON
OK

# Create a key and set its value to 100.
dragonfly> SET user_count 100
OK

# Read the key so that the server starts tracking its update.
dragonfly> GET user_count
"100"
```

Now `client-2` makes an update on the key:

```shell
### client-2 ###

# Now client-2 updates the value.
dragonfly> INCR user_count
(integer) 101
```

Back to `client-1` again, it reads the key (within the same session) and receives an invalidation message on the key:

```shell
### client-1 ###

# After client-2 updates the value,
# client-1 reads the key again and receives an invalidation message.
dragonfly> GET user_count
-> invalidate: 'user_count'
"101"
```
