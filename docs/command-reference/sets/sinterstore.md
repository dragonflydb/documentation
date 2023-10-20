---
description:  Learn how to use Redis SINTERSTORE command to find the intersection of sets and store the result.
---

import PageTitle from '@site/src/components/PageTitle';

# SINTERSTORE

<PageTitle title="Redis SINTERSTORE Command (Documentation) | Dragonfly" />

## Syntax

    SINTERSTORE destination key [key ...]

**Time complexity:** O(N*M) worst case where N is the cardinality of the smallest set and M is the number of sets.

**ACL categories:** @write, @set, @slow

This command is equal to `SINTER`, but instead of returning the resulting set,
it is stored in `destination`.

If `destination` already exists, it is overwritten.

## Return

[Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the number of elements in the resulting set.

## Examples

```shell
dragonfly> SADD key1 "a"
(integer) 1
dragonfly> SADD key1 "b"
(integer) 1
dragonfly> SADD key1 "c"
(integer) 1
dragonfly> SADD key2 "c"
(integer) 1
dragonfly> SADD key2 "d"
(integer) 1
dragonfly> SADD key2 "e"
(integer) 1
dragonfly> SINTERSTORE key key1 key2
(integer) 1
dragonfly> SMEMBERS key
1) "c"
```
