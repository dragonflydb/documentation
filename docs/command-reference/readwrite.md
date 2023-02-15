---
description: Disables read queries for a connection to a cluster replica node
---

# READWRITE

## Syntax

    READWRITE 

**Time complexity:** O(1)

Disables read queries for a connection to a Redis Cluster replica node.

Read queries against a Redis Cluster replica node are disabled by default,
but you can use the `READONLY` command to change this behavior on a per-
connection basis. The `READWRITE` command resets the readonly mode flag
of a connection back to readwrite.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings)
