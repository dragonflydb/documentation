---
description:  Learn how to use Redis SINTERCARD command to get the cardinality of intersection of multiple sets.
---

import PageTitle from '@site/src/components/PageTitle';

# SINTERCARD

<PageTitle title="Redis SINTERCARD Command (Documentation) | Dragonfly" />

## Syntax

    SINTERCARD numkeys key [key ...] [LIMIT limit]

**Time complexity:** O(N*M) worst case where N is the cardinality of the smallest set and M is the number of sets.

**ACL categories:** @read, @set, @slow

This command is similar to [`SINTER`](./sinter.md), but instead of returning the result set, it returns just the cardinality of the result.
Returns the cardinality of the set which would result from the intersection of all the given sets.

Keys that do not exist are considered to be empty sets.
With one of the keys being an empty set, the resulting set is also empty (since set intersection with an empty set always results in an empty set).

By default, the command calculates the cardinality of the intersection of all given sets.
When provided with the optional `LIMIT` argument (which defaults to `0` and means unlimited),
if the intersection cardinality reaches limit partway through the computation,
the algorithm will exit and yield limit as the cardinality.
Such implementation ensures a significant speedup for queries where the limit is lower than the actual intersection cardinality.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the cardinality (number of elements) of the set which would result from the intersection of all the given sets.

## Examples

```shell
dragonfly> SADD key1 "a"
(integer) 1
dragonfly> SADD key1 "b"
(integer) 1
dragonfly> SADD key1 "c"
(integer) 1
dragonfly> SADD key1 "d"
(integer) 1
dragonfly> SADD key2 "c"
(integer) 1
dragonfly> SADD key2 "d"
(integer) 1
dragonfly> SADD key2 "e"
(integer) 1
dragonfly> SINTER key1 key2
1) "c"
2) "d"
dragonfly> SINTERCARD 2 key1 key2
(integer) 2
dragonfly> SINTERCARD 2 key1 key2 LIMIT 1
(integer) 1
```
