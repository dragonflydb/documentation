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
 1) CLIENT &lt;subcommand&gt; [&lt;arg&gt; [value] [opt] ...]. Subcommands are:
 2) CACHING (YES|NO)
 3)     Enable/disable tracking of the keys for next command in OPTIN/OPTOUT modes.
 4) GETNAME
 5)     Return the name of the current connection.
 6) ID
 7)     Return the ID of the current connection.
 8) KILL &lt;ip:port&gt;
 9)     Kill connection made from &lt;ip:port&gt;.
10) KILL &lt;option&gt; &lt;value&gt; [&lt;option&gt; &lt;value&gt; [...]]
11)     Kill connections. Options are:
12)     * ADDR (&lt;ip:port&gt;|&lt;unixsocket&gt;:0)
13)       Kill connections made from the specified address
14)     * LADDR (&lt;ip:port&gt;|&lt;unixsocket&gt;:0)
15)       Kill connections made to specified local address
16)     * ID &lt;client-id&gt;
17)       Kill connections by client id.
18) LIST
19)     Return information about client connections.
20) UNPAUSE
21)     Stop the current client pause, resuming traffic.
22) PAUSE &lt;timeout&gt; [WRITE|ALL]
23)     Suspend all, or just write, clients for &lt;timeout&gt; milliseconds.
24) SETNAME &lt;name&gt;
25)     Assign the name &lt;name&gt; to the current connection.
26) SETINFO &lt;option&gt; &lt;value&gt;
27) Set client meta attr. Options are:
28)     * LIB-NAME: the client lib name.
29)     * LIB-VER: the client lib version.
30) TRACKING (ON|OFF) [OPTIN] [OPTOUT] [NOLOOP]
31)     Control server assisted client side caching.
32) MIGRATE &lt;client-id&gt; &lt;tid&gt;
33)     Migrates connection specified by client-id to the specified thread id.
34) HELP
35)     Print this help.
```

