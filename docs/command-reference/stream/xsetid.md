---
description: Set last id of a stream
---

# XSETID

## Syntax

	XSETID key last-id

**Time Complexity:** O(1)

**ACL categories:** @write, @stream, @fast

**XSETID** sets the last id of the specified stream. **<key\>**
must exists before executing the command. The **<last-id\>** can't
be smaller than target stream top entry.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings):
**OK** on success.
