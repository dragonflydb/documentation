---
description:  Learn how to use Redis SDIFF command to get the difference from the first set against all the other sets.
---

import PageTitle from '@site/src/components/PageTitle';

# SDIFF

<PageTitle title="Redis SDIFF Command (Documentation) | Dragonfly" />

## Syntax

    SDIFF key [key ...]

**Time complexity:** O(N) where N is the total number of elements in all given sets.

**ACL categories:** @read, @set, @slow

Returns the members of the set resulting from the difference between the first
set and all the successive sets.

For example:

```shell
key1 = {a,b,c,d}
key2 = {c}
key3 = {a,c,e}
SDIFF key1 key2 key3 = {b,d}
```

Keys that do not exist are considered to be empty sets.

## Return

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): list with members of the resulting set.

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
dragonfly> SDIFF key1 key2
1) "b"
2) "a"
```
