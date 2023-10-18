---
description: "Discover how to use Redis EXEC command to execute all commands issued after MULTI."
---

import PageTitle from '@site/src/components/PageTitle';

# EXEC

<PageTitle title="Redis EXEC Command (Documentation) | Dragonfly" />

## Syntax

    EXEC

**Time complexity:** Depends on commands in the transaction

**ACL categories:** @slow, @transaction

Executes all previously queued commands in a [transaction][tt] and restores the
connection state to normal.

[tt]: https://redis.io/topics/transactions

When using `WATCH`, `EXEC` will execute commands only if the watched keys were
not modified, allowing for a [check-and-set mechanism][ttc].

[ttc]: https://redis.io/topics/transactions#cas

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): each element being the reply to each of the commands in the
atomic transaction.

When using `WATCH`, `EXEC` can return a [Null reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings) if the execution was aborted.
