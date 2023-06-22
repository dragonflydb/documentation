---
description: Synchronously save the dataset to disk and then shut down the server
---

# SHUTDOWN

## Syntax

    SHUTDOWN [NOSAVE | SAVE]

**Time complexity:** O(1)


## Options

The `SHUTDOWN` command supports optional modifiers to alter the behavior of the command:

* `SAVE` will force a DB saving operation even if no save points are configured.
* `NOSAVE` will prevent a DB saving operation even if one or more save points are configured.


<!-- we dont do any of that useful stuff:

* If there are any replicas lagging behind in replication:
  * Pause clients attempting to write by performing a `CLIENT PAUSE` with the `WRITE` option.
  * Wait up to the configured `shutdown-timeout` (default 10 seconds) for replicas to catch up the replication offset.
* Stop all the clients.
* Perform a blocking SAVE if at least one **save point** is configured.
* Flush the Append Only File if AOF is enabled.
* Quit the server.

-->

Also note: If Dragonfly receives one of the signals `SIGTERM` and `SIGINT`, the same shutdown sequence is performed.
See also [Signal Handling](https://redis.io/topics/signals).

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK` if `ABORT` was specified and shutdown was aborted.
On successful shutdown, nothing is returned since the server quits and the connection is closed.
On failure, an error is returned.