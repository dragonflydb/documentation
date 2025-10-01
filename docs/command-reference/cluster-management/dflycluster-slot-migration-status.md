---
description:  Learn how to use Dragonfly DFLYCLUSTER SLOT-MIGRATION-STATUS to get status of the current migration on the node.
---

import PageTitle from '@site/src/components/PageTitle';

# DFLYCLUSTER SLOT-MIGRATION-STATUS

<PageTitle title="Dragonfly DFLYCLUSTER SLOT-MIGRATION-STATUS Command (Documentation) | Dragonfly" />

## Syntax

    DFLYCLUSTER SLOT-MIGRATION-STATUS [node_id]

**Time complexity:** O(N), where N is the number of migrations on the node

**ACL categories:** @admin, @slow

The `DFLYCLUSTER SLOT-MIGRATION-STATUS` command is used to get the status of one or all slot migrations on a Dragonfly node.
If a node_id is provided, the result shows the status of the migrations between the current node and the specified node_id. Otherwise, it returns the statuses of all migrations on the current node.

## Return

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): a nested list of migration info.
The next fields are presented:
* direction: in, out;
* node_id;
* state: CONNECTING, SYNC, ERROR, FINISHED, FATAL;
* keys_number: number of keys for selected slots on the current node;
* error: 0 if no errors happens, otherwise the last error description


## Examples

```shell
dragonfly> DFLYCLUSTER SLOT-MIGRATION-STATUS
1) 1) "out"
   2) "node_xfsef234fs"
   3) "SYNC"
   4) (integer) 2250125
   5) "0"

```
