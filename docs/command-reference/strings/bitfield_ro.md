---
description: Perform arbitrary bitfield integer operations on strings. Read-only
  variant of BITFIELD
---

# BITFIELD_RO

## Syntax

    BITFIELD_RO key [GET encoding offset [GET encoding offset ...]]

**Time complexity:** O(1) for each subcommand specified

**ACL categories:** @read, @bitmap, @fast

Read-only variant of the `BITFIELD` command.
It is like the original `BITFIELD` but only accepts `GET` subcommand and can safely be used in read-only replicas.

Since the original `BITFIELD` has `SET` and `INCRBY` options it is technically flagged as a writing command in the command table.
For this reason read-only replicas in a Dragonfly Cluster will redirect it to the master instance even if the connection is in read-only mode.

See original `BITFIELD` for more details.

## Examples

```
BITFIELD_RO hello GET i8 16
```

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): An array with each entry being the corresponding result of the subcommand given at the same position.
