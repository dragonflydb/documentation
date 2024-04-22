---
description: "Learn how the Redis TOUCH command alters the last access time of a key."
---

import PageTitle from '@site/src/components/PageTitle';

# TOUCH

<PageTitle title="Redis TOUCH Command (Documentation) | Dragonfly" />

## Syntax

    TOUCH key [key ...]

**Time complexity:** O(N) where N is the number of keys that will be touched.

**ACL categories:** @keyspace, @read, @fast

Alters the last access time of a key(s).
A key is ignored if it does not exist.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): The number of keys that were touched.

## Examples

```shell
dragonfly> SET key1 "Hello"
OK
dragonfly> SET key2 "World"
OK
dragonfly> TOUCH key1 key2
(integer) 2
```
