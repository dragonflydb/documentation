---
description:  Learn how to use Redis REPLCONF command for assisting in the replication process.
---

import PageTitle from '@site/src/components/PageTitle';

# REPLCONF

<PageTitle title="Redis REPLCONF Command (Documentation) | Dragonfly" />

## Syntax

    REPLCONF

**Time complexity:** O(1)

**ACL categories:** @admin, @slow, @dangerous

The `REPLCONF` command is an internal command.
It is used by a Dragonfly master to configure a connected replica.
