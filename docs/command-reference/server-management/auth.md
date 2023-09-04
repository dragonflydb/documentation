---
description: Authenticate to the server
---

# AUTH

## Syntax

    AUTH [username] password

**Time complexity:** O(1)

**ACL categories:** @fast, @connection

The AUTH command authenticates the current connection if the Dragonfly server is password protected via the `requirepass` option. Dragonfly will deny any command executed by the just
connected clients, unless the connection gets authenticated via `AUTH`.

If the password provided via AUTH matches the configured password, the server replies with the `OK` status code and starts accepting commands. Otherwise, an error is returned and the clients needs to try a new password.

Additionally, `AUTH` can be used to authenticate users created by the `ACL SETUSER` command.

## Security notice

Because of the high performance nature of Dragonfly, it is possible to try
a lot of passwords in parallel in very short time, so make sure to generate a
strong and very long password so that this attack is infeasible.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings) or an error if the password is invalid.
