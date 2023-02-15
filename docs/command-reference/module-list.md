---
description: List all modules loaded by the server
---

# MODULE LIST

## Syntax

    MODULE LIST 

**Time complexity:** O(N) where N is the number of loaded modules.

Returns information about the modules loaded to the server.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec#resp-arrays): list of loaded modules. Each element in the list represents a
module, and is in itself a list of property names and their values. The
following properties is reported for each loaded module:

*   `name`: Name of the module
*   `ver`: Version of the module
