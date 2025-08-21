---
description: "Learn to apply STICK command to prevent items from being evicted."
---

import PageTitle from '@site/src/components/PageTitle';

# STICK

<PageTitle title="Dragonfly STICK Command (Documentation) | Dragonfly" />

## Syntax

    STICK key [key ...]

**Time complexity:** O(N) where N is the number of keys that will be made sticky.

**ACL categories:** @keyspace, @write, @fast

Labels one or more keys as sticky, making it impossible for them to be evicted when the Dragonfly instance is running in cache mode.
This command is Dragonfly-specific.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): Number of keys that were made sticky successfully: those that existed and were not already sticky.

## Examples

```shell
dragonfly> MSET a 1 b 2
OK
dragonfly> STICK a
(integer) 1
dragonfly> STICK a b c
(integer) 1
```
