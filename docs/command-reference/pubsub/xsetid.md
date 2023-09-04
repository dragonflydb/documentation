---
description: An internal command for replicating stream values
---

# XSETID

## Syntax

    XSETID key last-id [ENTRIESADDED entries-added] [MAXDELETEDID max-deleted-id]

**Time complexity:** O(1)

**ACL categories:** @write, @stream, @fast

The `XSETID` command is an internal command.
It is used to replicate the last delivered ID of streams.
