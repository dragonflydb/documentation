---
description: "Understand the use of Redis UNLINK command to delete keys avoiding blocking operations."
---

import PageTitle from '@site/src/components/PageTitle';

# UNLINK

<PageTitle title="Redis UNLINK Command (Documentation) | Dragonfly" />

## Syntax

    UNLINK key [key ...]

**Time complexity:** O(N) where N is the number of keys that will be removed.

**ACL categories:** @keyspace, @write, @fast

This command is equivalent to `DEL` command, see `DEL` for more information.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): The number of keys that were unlinked.

## Examples

```shell
dragonfly> SET key1 "Hello"
OK
dragonfly> SET key2 "World"
OK
dragonfly> UNLINK key1 key2 key3
(integer) 2
```
