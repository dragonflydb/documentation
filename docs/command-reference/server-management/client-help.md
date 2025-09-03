---
description:  Learn how to use Redis CLIENT HELP command to list all CLIENT subcommands and their descriptions.
---

import PageTitle from '@site/src/components/PageTitle';

# CLIENT HELP

<PageTitle title="Redis CLIENT HELP Command (Documentation) | Dragonfly" />

## Syntax

    CLIENT HELP

**Time complexity:** O(1)

**ACL categories:** @slow

The `CLIENT HELP` command returns a helpful text describing the different `CLIENT` subcommands supported by Dragonfly.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a list of subcommands and their descriptions.

## Example

The output of the `CLIENT HELP` command includes entries similar to the following (as implemented in Dragonfly):

```shell
dragonfly> CLIENT HELP
 1) CLIENT <subcommand> [<arg> [value] [opt] ...]. Subcommands are:
 2) CACHING (YES|NO)
 3)     Enable/disable tracking of the keys for next command in OPTIN/OPTOUT modes.
 4) GETNAME
 5)     Return the name of the current connection.
 6) ID
 7)     Return the ID of the current connection.
 8) KILL <ip:port>
 9)     Kill connection made from <ip:port>.
10) KILL <option> <value> [<option> <value> [...]]
11)     Kill connections. Options are:
12)     * ADDR (<ip:port>|<unixsocket>:0)
13)       Kill connections made from the specified address
14)     * LADDR (<ip:port>|<unixsocket>:0)
15)       Kill connections made to specified local address
16)     * ID <client-id>
17)       Kill connections by client id.
18) LIST
19)     Return information about client connections.
20) UNPAUSE
21)     Stop the current client pause, resuming traffic.
22) PAUSE <timeout> [WRITE|ALL]
23)     Suspend all, or just write, clients for <timeout> milliseconds.
24) SETNAME <name>
25)     Assign the name <name> to the current connection.
26) SETINFO <option> <value>
27) Set client meta attr. Options are:
28)     * LIB-NAME: the client lib name.
29)     * LIB-VER: the client lib version.
30) TRACKING (ON|OFF) [OPTIN] [OPTOUT] [NOLOOP]
31)     Control server assisted client side caching.
32) MIGRATE <client-id> <tid>
33)     Migrates connection specified by client-id to the specified thread id.
34) HELP
35)     Print this help.
```
