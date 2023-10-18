---
description:  Learn how to use Redis CONFIG SET command to set the configuration of the server.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG SET

<PageTitle title="Redis CONFIG SET Command (Documentation) | Dragonfly" />

## Syntax

    CONFIG SET parameter value [parameter value ...]

**Time complexity:** O(N) when N is the number of configuration parameters provided

**ACL categories:** @admin, @slow, @dangerous

The `CONFIG SET` command is used in order to reconfigure the server at runtime without the need to restart Dragonfly.

The list of configuration parameters supported by `CONFIG SET` can be obtained by issuing the `CONFIG GET *` command,
which is the symmetrical command used to obtain information about the configuration of a running Dragonfly instance.
See the [`CONFIG GET` documentation](./config-get.md) for more details.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): `OK` when the configuration was set properly, error otherwise.

## Examples

```shell
dragonfly> CONFIG SET maxmemory 10gb maxclients 32000
OK

dragonfly> CONFIG GET *
 1) "maxmemory"
 2) "10.00GiB"
 3) "tcp_keepalive"
 4) "300"
 5) "dbnum"
 6) "16"
 7) "maxclients"
 8) "32000"
 9) "dir"
10) "./data"
11) "masterauth"
12) ""
13) "requirepass"
14) ""
```
