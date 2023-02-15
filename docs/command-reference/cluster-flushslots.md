---
description: Delete a node's own slots information
---

# CLUSTER FLUSHSLOTS

## Syntax

    CLUSTER FLUSHSLOTS 

**Time complexity:** O(1)

Deletes all slots from a node.

The `CLUSTER FLUSHSLOTS` deletes all information about slots from the connected node. It can only be called when the database is empty.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK`
