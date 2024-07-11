---
description: "Learn to use Redis UNWATCH command that flushes all previously watched keys."
---

import PageTitle from '@site/src/components/PageTitle';

# UNWATCH

<PageTitle title="Redis UNWATCH Command (Documentation) | Dragonfly" />

## Syntax

    UNWATCH

**Time complexity:** O(1)

**ACL categories:** @fast, @transaction

Flushes all the previously watched keys for a [transaction][tt].

[tt]: https://redis.io/topics/transactions

If you call `EXEC` or `DISCARD`, there's no need to manually call `UNWATCH`.

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): always `OK`.
