---
description: Close the connection
---

# QUIT

## Syntax

    QUIT 

**Time complexity:** O(1)

**ACL categories:** @fast, @connection

Ask the server to close the connection.
The connection is closed as soon as all pending replies have been written to the
client.

**Note:** Clients should not use this command.
Instead, clients should simply close the connection when they're not used anymore.
Terminating a connection on the client side is preferable, as it eliminates `TIME_WAIT` lingering sockets on the server side.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): always OK.
