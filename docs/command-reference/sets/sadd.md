---
description:  Learn how to use Redis SADD command to add one or more members to a set.
---

import PageTitle from '@site/src/components/PageTitle';

# SADD

<PageTitle title="Redis SADD Command (Documentation) | Dragonfly" />

## Syntax

    SADD key member [member ...]

**Time complexity:** O(1) for each element added, so O(N) to add N elements when the command is called with multiple arguments.

**ACL categories:** @write, @set, @fast

Add the specified members to the set stored at `key`.
Specified members that are already a member of this set are ignored.
If `key` does not exist, a new set is created before adding the specified
members.

An error is returned when the value stored at `key` is not a set.

## Return

[Integer reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#integers): the number of elements that were added to the set, not including
all the elements already present in the set.

## Examples

```shell
dragonfly> SADD myset "Hello"
(integer) 1
dragonfly> SADD myset "World"
(integer) 1
dragonfly> SADD myset "World"
(integer) 0
dragonfly> SMEMBERS myset
1) "Hello"
2) "World"
```
