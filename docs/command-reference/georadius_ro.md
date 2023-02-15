---
description: A read-only variant for GEORADIUS
---

# GEORADIUS_RO

## Syntax

    GEORADIUS_RO key longitude latitude radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC]

**Time complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

Read-only variant of the `GEORADIUS` command.

This command is identical to the `GEORADIUS` command, except that it doesn't support the optional `STORE` and `STOREDIST` parameters.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): An array with each entry being the corresponding result of the subcommand given at the same position.
