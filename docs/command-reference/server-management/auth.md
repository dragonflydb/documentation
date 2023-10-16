---
description: Authenticate to the server
---

# AUTH

## Syntax

    AUTH [username] password

**Time complexity:** O(1)

**ACL categories:** @fast, @connection

The AUTH command authenticates the current connection. If the `username` is omitted, it implies the user `default` from ACL. Dragonfly will deny any command executed by the just
connected clients, unless the connection gets authenticated via `AUTH`.

If the password provided via AUTH matches the configured password, the server replies with the `OK` status code and starts accepting commands. Otherwise, an error is returned and the clients needs to try a new password.

Note, that `requirepass` now also changes the ACL default user `password`.

## Security notice

Because of the high performance nature of Dragonfly, it is possible to try
a lot of passwords in parallel in very short time, so make sure to generate a
strong and very long password so that this attack is infeasible.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings) or an error if the password is invalid.
