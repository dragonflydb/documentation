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

[tt]: https://redis.io/topics/transactions

## Return

[Simple string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#simple-strings): always `OK`.
