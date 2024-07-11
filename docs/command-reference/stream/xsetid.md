---
description:  Learn how to use Redis XSETID to set the last delivered ID for streams.
---

import PageTitle from '@site/src/components/PageTitle';

# XSETID

<PageTitle title="Redis XSETID Command (Documentation) | Dragonfly" />

## Syntax

	XSETID key last-id

**Time Complexity:** O(1)

**ACL categories:** @write, @stream, @fast

**XSETID** sets the last id of the specified stream. **<key\>**
must exists before executing the command. The **<last-id\>** can't
be smaller than target stream top entry.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings):
**OK** on success.
