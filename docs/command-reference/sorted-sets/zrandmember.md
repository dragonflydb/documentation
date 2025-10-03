---
description:  Learn how to get random members of a sorted set with the Dragonfly ZRANDMEMBER command.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANDMEMBER

<PageTitle title="Dragonfly ZRANDMEMBER Command (Documentation) | Dragonfly" />

## Syntax

```shell
    ZRANDMEMBER key [count [WITHSCORES]]
```

**Time complexity:** O(N) where N is the number of members returned

**ACL categories:** @read, @sortedset, @slow

When called with just the `key` argument, return a random element from the sorted set value stored at `key`.

If the provided `count` argument is positive, return an array of distinct elements. The array's length is either `count` or the sorted set's cardinality ([`ZCARD`](./zcard.md)), whichever is lower.

If called with a negative `count`, the behavior changes and the command is allowed to return the same element multiple times. In this case, the number of returned elements is the absolute value of the specified `count`.

The optional WITHSCORES modifier changes the reply so it includes the respective scores of the randomly selected elements from the sorted set.

## Return

When called without the `count` argument:

[Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): the random member, or `nil` when `key` does not exist.

When called with the `count` argument:

[Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): the random members, or an empty array when `key` does not exist.  If the WITHSCORES modifier is used, the reply is a list of members and their scores from the sorted set.

## Examples

```shell
dragonfly> ZADD numbers 1 one 2 two 3 three 4 four
(integer) 4
dragonfly> ZRANDMEMBER numbers
1) "one"
dragonfly> ZRANDMEMBER numbers 2
1) "two"
2) "three"
dragonfly> ZRANDMEMBER numbers -3
1) "three"
2) "three"
3) "four"
dragonfly> ZRANDMEMBER numbers 3 WITHSCORES
1) "two"
2) "2"
3) "three"
4) "3"
5) "four"
6) "4"
```