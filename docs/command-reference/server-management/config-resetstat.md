---
description: Reset the stats returned by INFO
---

# CONFIG RESETSTAT

## Syntax

    CONFIG RESETSTAT 

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

Resets the statistics reported by Dragonfly using the `INFO` command.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): always `OK`.
