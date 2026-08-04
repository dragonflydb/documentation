---
description: "Check the status of an in-progress hash slot migration on a Dragonfly cluster node."
---

import PageTitle from '@site/src/components/PageTitle';

# DFLYCLUSTER SLOT-MIGRATION-STATUS

<PageTitle title="Dragonfly DFLYCLUSTER SLOT-MIGRATION-STATUS Command (Documentation) | Dragonfly" />

## Syntax

    DFLYCLUSTER SLOT-MIGRATION-STATUS [node_id]

**Time complexity:** O(M + R), where M is the number of migrations on the
node and R is the total number of their slot ranges.

**ACL categories:** @admin, @slow

The `DFLYCLUSTER SLOT-MIGRATION-STATUS` command is used to get the status of one or all slot migrations on a Dragonfly node.
If a `node_id` is provided, the result shows the status of the migrations between the current node and the specified `node_id`.
Otherwise, it returns the statuses of all migrations on the current node.

## Return

[Array reply](https://valkey.io/topics/protocol/#arrays): a nested list of migration info.
For each migration, the following fields are returned:
- The migration direction, which can be `in` or `out`.
- The `node_id` of the migration.
- The migration state, which can be `CONNECTING`, `SYNC`, `ERROR`, `FINISHED`, or `FATAL`.
- The number of keys for selected slots on the current node.
- The error status, which is `0` when no error occurred. Otherwise, it shows the last error description.
- The slot ranges included in the migration, formatted as a string.

## Examples

```shell
# The current node finished migrating four keys in slots 3000 through 9000.
dragonfly> DFLYCLUSTER SLOT-MIGRATION-STATUS
1) 1) "out"
   2) "133807dea9b616400e22587b99abd87a1cbf6473"
   3) "FINISHED"
   4) (integer) 4
   5) "0"
   6) "[3000, 9000]"
```
