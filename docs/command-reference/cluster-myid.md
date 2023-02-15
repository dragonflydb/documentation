---
description: Return the node id
---

# CLUSTER MYID

## Syntax

    CLUSTER MYID 

**Time complexity:** O(1)

Returns the node's id.

The `CLUSTER MYID` command returns the unique, auto-generated identifier that is associated with the connected cluster node.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): The node id.