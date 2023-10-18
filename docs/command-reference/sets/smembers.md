---
description:  Learn how to get all members of a set with the Redis SMEMBERS command.
---

import PageTitle from '@site/src/components/PageTitle';

# SMEMBERS

<PageTitle title="Redis SMEMBERS Command (Documentation) | Dragonfly" />

## Syntax

    SMEMBERS key

**Time complexity:** O(N) where N is the set cardinality.

**ACL categories:** @read, @set, @slow

Returns all the members of the set value stored at `key`.

This has the same effect as running `SINTER` with one argument `key`.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): all elements of the set.

## Examples

```shell
dragonfly> SADD myset "Hello"
(integer) 1
dragonfly> SADD myset "World"
(integer) 1
dragonfly> SMEMBERS myset
1) "Hello"
2) "World"
```
