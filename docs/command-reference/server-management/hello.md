---
description: Handshake with Dragonfly
---

# HELLO

## Syntax

    HELLO

**Time complexity:** O(1)

Provide a contextual client report.

`HELLO` always replies with a list of current server and connection properties,
such as: versions, modules loaded, client ID, replication role and so forth.
The reply looks like this:

    > HELLO
     1) "server"
     2) "redis"
     3) "version"
     4) "df-dev"
     5) "proto"
     6) (integer) 2
     7) "id"
     8) (integer) 5
     9) "mode"
    1)  "standalone"
    2)  "role"
    3)  "master"

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): a list of server properties. The command returns an error if the `protover` requested does not exist.
