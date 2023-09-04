---
description: An internal command for configuring the replication stream
---

# REPLCONF

## Syntax

    REPLCONF 

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

The `REPLCONF` command is an internal command.
It is used by a Dragonfly master to configure a connected replica.
