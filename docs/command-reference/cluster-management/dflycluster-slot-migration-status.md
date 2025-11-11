---
description: Get migration status of the current node.
---

import PageTitle from '@site/src/components/PageTitle';

# DFLYCLUSTER SLOT-MIGRATION-STATUS

<PageTitle title="Dragonfly DFLYCLUSTER SLOT-MIGRATION-STATUS Command (Documentation) | Dragonfly" />

## Syntax

    DFLYCLUSTER SLOT-MIGRATION-STATUS [node_id]

**Time complexity:** O(N), where N is the number of migrations on the node

**ACL categories:** @admin, @slow

The `DFLYCLUSTER SLOT-MIGRATION-STATUS` command is used to get the status of one or all slot migrations on a Dragonfly node.
If a `node_id` is provided, the result shows the status of the migrations between the current node and the specified `node_id`.
Otherwise, it returns the statuses of all migrations on the current node.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a nested list of migration info.
For each migration, the following fields are returned:
- The migration direction, which can be `in` or `out`.
- The `node_id` of the migration.
- The migration state, which can be `CONNECTING`, `SYNC`, `ERROR`, `FINISHED`, or `FATAL`.
- The number of keys for selected slots on the current node.
- The error status, which is `0` if no error happens. Otherwise, it shows the last error description.

## Examples

```shell
# The current node is migrating out to 'node_xfsef234fs'.
# It is currently syncing the data of 2250125 keys.
dragonfly> DFLYCLUSTER SLOT-MIGRATION-STATUS
1) 1) "out"
   2) "node_xfsef234fs"
   3) "SYNC"
   4) (integer) 2250125
   5) "0"
```
