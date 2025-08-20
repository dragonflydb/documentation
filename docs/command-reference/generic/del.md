---
description: "Learn how to use Redis DEL command to delete a key."
---

import PageTitle from '@site/src/components/PageTitle';

# DEL

<PageTitle title="Redis DEL Command (Documentation) | Dragonfly" />

## Syntax

    DEL key [key ...]

**Time complexity:** O(N) where N is the number of keys that will be removed. When a key to remove holds a value other than a string, the individual complexity for this key is O(M) where M is the number of elements in the list, set, sorted set or hash. Removing a single key that holds a string value is O(1).

**ACL categories:** @keyspace, @write, @slow

Removes the specified keys.
A key is ignored if it does not exist.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): The number of keys that were removed.

## Examples

```shell
dragonfly> SET key1 "Hello"
OK
dragonfly> SET key2 "World"
OK
dragonfly> DEL key1 key2 key3
(integer) 2
```
