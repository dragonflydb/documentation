---
description:  Learn how to use Redis CLIENT TRACKING command to control server-assisted client side caching for the connection.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT TRACKING

<PageTitle title="Redis CLIENT TRACKING Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT TRACKING <ON | OFF>

**Time complexity:** O(1). Some options may introduce additional complexity.

**ACL categories:** @slow, @connection

**Important**: New in Dragonfly v1.14, only available when the [RESP3](https://github.com/redis/redis-specifications/blob/master/protocol/RESP3.md) protocol is used.

The `CLIENT TRACKING` command enables the tracking feature of the Dragonfly server, which is used for server-assisted client side caching.
See more details about server-assisted client side caching in the [Redis documentation](https://redis.io/docs/manual/client-side-caching/).

When tracking is enabled, Dragonfly remembers the keys that the connection requested in order to send later invalidation messages when such keys are modified.
Invalidation messages are sent in the same connection when the RESP3 protocol is used.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` if the connection was
successfully put in tracking mode or if the tracking mode was successfully disabled. Otherwise, an error is returned.

## Examples

Use two clients to connect to the Dragonfly server using the RESP3 protocol.
Switching to the RESP3 protocol can be done with the `HELLO` command.
Alternatively, clients or SDKs may have a configuration option to use the RESP3 protocol (i.e., `redis-cli -3`) upon connection.

In the example below, the first client is put in tracking mode.
When the second client updates a key, the first client will receive an invalidation message.
Note that creating a non-existing key will not make Dragonfly track the key.
A key must be read by the client to be tracked.

```shell
### client-1 ###

# Switch protocol to RESP3, output omitted.
dragonfly> HELLO 3

# Create a key, set its value, and read it back.
dragonfly> SET user_count 100
OK
dragonfly> GET user_count
"100"

# After client-2 updates the value, read the key again.
dragonfly> GET user_count
-> invalidate: 'user_count'
"101"
```

```shell
### client-2 ###

# Switch protocol to RESP3, output omitted.
dragonfly> HELLO 3

# Now client-2 updates the value.
dragonfly> INCR user_count
(integer) 101
```
