---
description: "Discover the Redis MULTI command used for transactions."
---

import PageTitle from '@site/src/components/PageTitle';

# MULTI

<PageTitle title="Redis MULTI Command (Documentation) | Dragonfly" />

## Syntax

    MULTI

**Time complexity:** O(1)

**ACL categories:** @fast, @transaction

Marks the start of a [transaction][tt] block.
Subsequent commands will be queued for atomic execution using `EXEC`.
If a command is rejected while queuing (for example, an unknown command or a wrong number of arguments), `EXEC` aborts the transaction instead of executing the queued commands. The error from a nested `MULTI` call does not abort the transaction.

[tt]: https://redis.io/topics/transactions

## Return

[Simple string reply](https://valkey.io/topics/protocol/#simple-strings): `OK` when the transaction starts.

An error reply is returned if `MULTI` is called inside an existing transaction because transactions cannot be nested.
