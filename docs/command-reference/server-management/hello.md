---
description:  Learn how to use Redis HELLO command as a handshake for the Redis protocol.
---

import PageTitle from '@site/src/components/PageTitle';

# HELLO

<PageTitle title="Redis HELLO Command (Documentation) | Dragonfly" />

## Syntax

    HELLO [protover [AUTH username password] [SETNAME clientname]]

**Time complexity:** O(1)

**ACL categories:** @fast, @connection

Switch to a different protocol, optionally authenticating and setting the connection's name, or provide a contextual client report.

Dragonfly supports two protocols: RESP2 and RESP3.

Connections start in RESP2 mode, so clients implementing RESP2 do not need to updated or changed.

`HELLO` always replies with a list of current server and connection properties,
such as: versions, modules loaded, client ID, replication role and so forth.
The reply looks like this:


```shell
dragonfly> HELLO
 1) "server"
 2) "redis"
 3) "version"
 4) "6.2.11"
 5) "dfly_version"
 6) "df-dev"
 7) "proto"
 8) (integer) 2
 9) "id"
10) (integer) 1
11) "mode"
12) "standalone"
13) "role"
14) "master"
```


Clients that want to handshake using the RESP3 mode need to call the HELLO command and specify the value "3" as the protover argument , like so:

```shell
dragonfly> HELLO 3
1# "server" => "redis"
2# "version" => "6.2.11"
3# "dfly_version" => "df-dev"
4# "proto" => (integer) 3
5# "id" => (integer) 1
6# "mode" => "standalone"
7# "role" => "master"
```

Because `HELLO` replies with useful information, and given that protover is optional or can be set to "2", client library authors may consider using this command instead of the canonical `PING` when setting up the connection.

When called with the optional protover argument, this command switches the protocol to the specified version and also accepts the following options:

`AUTH <username> <password>`: directly authenticates the connection in addition to switching to the specified protocol version. This makes calling `AUTH` before `HELLO` unnecessary when setting up a new connection. Note that the default username is `default` as Dragonfly has built in support for ACLs.
`SETNAME <clientname>`: this is the equivalent of calling CLIENT SETNAME.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of server properties. The reply is a map instead of an array when RESP3 is selected. The command returns an error if the protover requested does not exist.
