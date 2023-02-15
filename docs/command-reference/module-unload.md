---
description: Unload a module
---

# MODULE UNLOAD

## Syntax

    MODULE UNLOAD name

**Time complexity:** O(1)

Unloads a module.

This command unloads the module specified by `name`. Note that the module's name
is reported by the `MODULE LIST` command, and may differ from the dynamic
library's filename.

Known limitations:

*   Modules that register custom data types can not be unloaded.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec#resp-simple-strings): `OK` if module was unloaded.
