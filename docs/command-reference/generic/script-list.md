---
description: List all scripts in the script cache.
---

# SCRIPT LIST

## Syntax

    SCRIPT LIST

**Time complexity:** O(N) with N being the number of scripts in script cache.

**ACL categories:** @slow, @scripting

Returns information about all the scripts in the script cache.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays) This command returns an array of elements. The first element is the SHA1 digest of the scripts added into the script cache. The second element is lua script.
