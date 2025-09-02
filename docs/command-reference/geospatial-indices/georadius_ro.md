---
description: "Learn how to use GEORADIUS_RO to find geographical data in your Dragonfly database by defining latitude and longitude."
---

import PageTitle from '@site/src/components/PageTitle';

# GEORADIUS_RO
 
<PageTitle title="GEORADIUS_RO Command (Documentation) | Dragonfly" />

## Syntax

    GEORADIUS_RO key longitude latitude radius <M | KM | FT | MI> [WITHCOORD] [WITHDIST] [WITHHASH] [COUNT count [ANY]] [ASC | DESC]

**Time complexity:** O(N+log(M)) where N is the number of elements inside the bounding box of the circular area delimited by center and radius and M is the number of items inside the index.

**ACL categories:** @read, @geo, @slow

Read-only variant of the [`GEORADIUS`](./georadius.md) command.

This command is identical to the [`GEORADIUS`](./georadius.md) command, except that it doesn't support the optional `STORE` and `STOREDIST` parameters.
