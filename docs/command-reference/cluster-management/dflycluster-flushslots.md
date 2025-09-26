---
description:  Learn how to use Dragonfly DFLYCLUSTER FLUSHSLOTS to get status of the current migration on the node.
---

import PageTitle from '@site/src/components/PageTitle';

# DFLYCLUSTER FLUSHSLOTS

<PageTitle title="Dragonfly DFLYCLUSTER FLUSHSLOTS Command (Documentation) | Dragonfly" />

## Syntax

    DFLYCLUSTER FLUSHSLOTS start_slot end_slot [start_slot end_slot ...]

**Time complexity:** O(N) where N is the total number of keys in selected slots

**ACL categories:** @keyspace, @write, @slow, @dangerous

Delete all the keys of selected slots.
This command never fails.

Note: command only deletes keys that were present at the time the command was invoked. Keys created during an asynchronous flush will be unaffected.

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings)