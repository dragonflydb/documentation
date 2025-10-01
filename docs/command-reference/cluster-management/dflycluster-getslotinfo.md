---
description:  Learn how to use Dragonfly DFLYCLUSTER GETSLOTINFO to get status of the current migration on the node.
---

import PageTitle from '@site/src/components/PageTitle';

# DFLYCLUSTER GETSLOTINFO

<PageTitle title="Dragonfly DFLYCLUSTER GETSLOTINFO Command (Documentation) | Dragonfly" />

## Syntax

    DFLYCLUSTER GETSLOTINFO SLOTS slot [slot ...]

**Time complexity:** O(N) where N is the number of provided slots

**ACL categories:**  @admin, @slow

The `DFLYCLUSTER GETSLOTINFO` command is used to get information regarding provided slots.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a nested list of slots info.


## Examples

```shell
dragonfly> DFLYCLUSTER GETSLOTINFO SLOTS 1 12
1) 1) (integer) 1
   2) "key_count"
   3) (integer) 1
   4) "total_reads"
   5) (integer) 1
   6) "total_writes"
   7) (integer) 2
   8) "memory_bytes"
   9) (integer) 84
2) 1) (integer) 12
   2) "key_count"
   3) (integer) 6
   4) "total_reads"
   5) (integer) 6
   6) "total_writes"
   7) (integer) 23
   8) "memory_bytes"
   9) (integer) 933

```
