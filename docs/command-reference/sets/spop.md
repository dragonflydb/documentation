---
description:  Learn how to remove and return random members from a set with Redis SPOP command.
---

import PageTitle from '@site/src/components/PageTitle';

# SPOP

<PageTitle title="Redis SPOP Command (Documentation) | Dragonfly" />

## Syntax

    SPOP key [count]

**Time complexity:** Without the count argument O(1), otherwise O(N) where N is the value of the passed count.

**ACL categories:** @write, @set, @fast

Removes and returns one or more random members from the set value store at `key`.

This operation is similar to `SRANDMEMBER`, that returns one or more random elements from a set but does not remove it.

By default, the command pops a single member from the set. When provided with
the optional `count` argument, the reply will consist of up to `count` members,
depending on the set's cardinality.

## Return

When called without the `count` argument:

[Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): the removed member, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://redis.io/docs/reference/protocol-spec/#arrays): the removed members, or an empty array when `key` does not exist.

## Examples

```shell
dragonfly> SADD myset "one"
(integer) 1
dragonfly> SADD myset "two"
(integer) 1
dragonfly> SADD myset "three"
(integer) 1
dragonfly> SPOP myset
"one"
dragonfly> SMEMBERS myset
1) "three"
2) "two"
dragonfly> SADD myset "four"
(integer) 1
dragonfly> SADD myset "five"
(integer) 1
dragonfly> SPOP myset 3
1) "three"
2) "two"
3) "four"
dragonfly> SMEMBERS myset
1) "five"
```
## Distribution of returned elements

Note that this command is not suitable when you need a guaranteed uniform distribution of the returned elements. For more information about the algorithms used for `SPOP`, look up both the Knuth sampling and Floyd sampling algorithms.
