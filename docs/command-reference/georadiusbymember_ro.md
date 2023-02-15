---
description: A read-only variant for GEORADIUSBYMEMBER
---

# GEORADIUSBYMEMBER_RO

## Syntax

    GEORADIUSBYMEMBER_RO key member radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC]

**Time complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

Read-only variant of the `GEORADIUSBYMEMBER` command.

This command is identical to the `GEORADIUSBYMEMBER` command, except that it doesn't support the optional `STORE` and `STOREDIST` parameters.
