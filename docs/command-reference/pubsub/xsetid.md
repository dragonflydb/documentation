---
description:  Learn how to use Redis XSETID to set the last delivered ID for streams.
---
import PageTitle from '@site/src/components/PageTitle';

# XSETID

<PageTitle title="Redis XSETID Command (Documentation) | Dragonfly" />

## Syntax

    XSETID key last-id [ENTRIESADDED entries-added] [MAXDELETEDID max-deleted-id]

**Time complexity:** O(1)

**ACL categories:** @write, @stream, @fast

The `XSETID` command is an internal command.
It is used to replicate the last delivered ID of streams.
