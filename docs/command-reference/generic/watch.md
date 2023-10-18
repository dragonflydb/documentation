---
description: "Learn the use of Redis WATCH command to monitor keys for conditional transactions."
---

import PageTitle from '@site/src/components/PageTitle';

# WATCH

<PageTitle title="Redis WATCH Command (Documentation) | Dragonfly" />

## Syntax

    WATCH key [key ...]

**Time complexity:** O(1) for every key.

**ACL categories:** @fast, @transaction

Marks the given keys to be watched for conditional execution of a
[transaction][tt].

[tt]: https://redis.io/topics/transactions

## Return

[Simple string reply](https://redis.io/docs/reference/protocol-spec/#simple-strings): always `OK`.
