---
description: "Understand Redis SCRIPT EXISTS command for checking scripts' existence in the cache."
---

import PageTitle from '@site/src/components/PageTitle';

# SCRIPT EXISTS

<PageTitle title="Redis SCRIPT EXISTS Command (Documentation) | Dragonfly" />

## Syntax

    SCRIPT EXISTS sha1 [sha1 ...]

**Time complexity:** O(N) with N being the number of scripts to check (so checking a single script is an O(1) operation).

**ACL categories:** @slow, @scripting

Returns information about the existence of the scripts in the script cache.

This command accepts one or more SHA1 digests and returns a list of ones or
zeros to signal if the scripts are already defined or not inside the script
cache.
This can be useful before a pipelining operation to ensure that scripts are
loaded (and if not, to load them using `SCRIPT LOAD`) so that the pipelining
operation can be performed solely using `EVALSHA` instead of `EVAL` to save
bandwidth.

For more information about `EVAL` scripts please refer to [Introduction to Eval Scripts](https://redis.io/docs/latest/develop/interact/programmability/eval-intro/).

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays) The command returns an array of integers that correspond to
the specified SHA1 digest arguments.
For every corresponding SHA1 digest of a script that actually exists in the
script cache, a 1 is returned, otherwise 0 is returned.
