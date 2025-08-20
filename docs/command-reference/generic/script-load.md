---
description: "Learn to use the Redis SCRIPT LOAD command which loads a script into cache."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT LOAD

<PageTitle title="Redis SCRIPT LOAD Command (Documentation) | Dragonfly" />

## Syntax

    SCRIPT LOAD script

**Time complexity:** O(N) with N being the length in bytes of the script body.

**ACL categories:** @slow, @scripting

Load a script into the scripts cache, without executing it.
After the specified command is loaded into the script cache it will be callable
using `EVALSHA` with the correct SHA1 digest of the script, exactly like after
the first successful invocation of `EVAL`.

The script is guaranteed to stay in the script cache forever (unless `SCRIPT
FLUSH` is called).

The command works in the same way even if the script was already present in the
script cache.

For more information about `EVAL` scripts please refer to [Introduction to Eval Scripts](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/).

## Return

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings) This command returns the SHA1 digest of the script added into the
script cache.
