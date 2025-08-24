---
description:  Learn how to use Redis CLIENT KILL command to terminate client connections by filters.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT KILL

<PageTitle title="Redis CLIENT KILL Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT KILL ip:port
    CLIENT KILL ADDR ip:port
    CLIENT KILL LADDR ip:port
    CLIENT KILL ID client-id

**Time complexity:** O(N) where N is the number of client connections.

**ACL categories:** @admin, @slow, @dangerous, @connection

Terminate client connections that match the specified filter.

Dragonfly supports the following filters:

- ADDR ip:port: kill connections made from the specified remote address.
- LADDR ip:port: kill connections made to the specified local bind address.
- ID client-id: kill a specific client by numeric id.
- A single `ip:port` argument is equivalent to `ADDR ip:port`.

Unsupported filters from Redis/Valkey (such as USER/TYPE/SKIPME) are currently not implemented in Dragonfly.

Admin-protected connections cannot be killed by non-privileged clients. If the request attempts to kill admin connections, the command returns an error indicating how many were not terminated.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the number of client connections that were terminated.

If some admin connections could not be killed by a non-privileged client.

## Examples

```shell
dragonfly> CLIENT KILL 127.0.0.1:6380
(integer) 1

dragonfly> CLIENT KILL ADDR 10.0.0.5:6379
(integer) 1

dragonfly> CLIENT KILL LADDR 127.0.0.1:6379
(integer) 1

dragonfly> CLIENT KILL ID 42
(integer) 1
```

## Notes

- The command affects only connections that exist at the time of execution.
- For bulk termination, prefer using `ADDR`/`LADDR` filters.
- Behavior may differ from Redis/Valkey for unsupported filters.
