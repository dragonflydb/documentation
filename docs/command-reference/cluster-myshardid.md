---
description: Return the node shard id
---

# CLUSTER MYSHARDID

## Syntax

    CLUSTER MYSHARDID 

**Time complexity:** O(1)

Returns the node's shard id.

The `CLUSTER MYSHARDID` command returns the unique, auto-generated identifier that is associated with the shard to which the connected cluster node belongs.

## Return

[Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): The node's shard id.
