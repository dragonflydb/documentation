---
description: Reset the stats returned by INFO
---

# CONFIG RESETSTAT

## Syntax

    CONFIG RESETSTAT 

**Time complexity:** O(1)

Resets the statistics reported by Dragonfly using the `INFO` command.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): always `OK`.
