---
description:  Learn how to use Redis CONFIG GET command to retrieve configuration parameters.
---

import PageTitle from '@site/src/components/PageTitle';

# CONFIG GET

<PageTitle title="Redis CONFIG GET Command (Documentation) | Dragonfly" />

## Syntax

    CONFIG GET parameter

**Time complexity:** O(N) when N is the number of configuration parameters provided

**ACL categories:** @admin, @slow, @dangerous

The `CONFIG GET` command is used to read the configuration parameters of a running Dragonfly server.

The symmetric command used to alter the configuration at runtime is [`CONFIG SET`](./config-set.md).

`CONFIG GET` takes a single argument, which uses the glob-style pattern.
Any configuration parameters matching the pattern are reported as a list of key-value pairs.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): list of key-value pairs for configuration parameters.

## Examples

Use the command and glob-style pattern below to read configuration parameters that are prefixed with `max`.

```shell
dragonfly> CONFIG GET max*
1) "maxmemory"
2) "12.11GiB"
3) "maxclients"
4) "64000"
```

You can also read all the supported configuration parameters by using the `*` wildcard.

```shell
dragonfly> CONFIG GET *
 1) "maxmemory"
 2) "32.00GiB"
 3) "tcp_keepalive"
 4) "300"
 5) "dbnum"
 6) "16"
 7) "maxclients"
 8) "64000"
 9) "dir"
10) "./data"
11) "masterauth"
12) ""
13) "requirepass"
14) ""
```
