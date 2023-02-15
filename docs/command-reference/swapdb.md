---
description: Swaps two Redis databases
---

# SWAPDB

## Syntax

    SWAPDB index1 index2

**Time complexity:** O(N) where N is the count of clients watching or blocking on keys from both databases.

This command swaps two Redis databases, so that immediately all the
clients connected to a given database will see the data of the other database, and
the other way around. Example:

    SWAPDB 0 1

This will swap database 0 with database 1. All the clients connected with database 0 will immediately see the new data, exactly like all the clients connected with database 1 will see the data that was formerly of database 0.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK` if `SWAPDB` was executed correctly.

## Examples

```
SWAPDB 0 1
```
