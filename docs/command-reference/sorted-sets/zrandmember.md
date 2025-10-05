---
description:  Learn how to get random members of a sorted set with the Dragonfly ZRANDMEMBER command.
---

import PageTitle from '@site/src/components/PageTitle';

# ZRANDMEMBER

<PageTitle title="Dragonfly ZRANDMEMBER Command (Documentation) | Dragonfly" />

## Introduction

In Dragonfly, as well as in Redis and Valkey, the `ZRANDMEMBER` command is used to return one or more random members from a sorted set.
It provides flexibility for both sampling single and multiple elements, with or without their associated scores.

## Syntax

```shell
ZRANDMEMBER key [count [WITHSCORES]]
```

**Time complexity:** O(N) where N is the number of members returned

**ACL categories:** @read, @sortedset, @slow

When called with just the `key` argument, return a random element from the sorted set value stored at `key`.

If the provided `count` argument is positive, return an array of distinct elements. The array's length is either `count` or the sorted set's cardinality ([`ZCARD`](./zcard.md)), whichever is lower.

If called with a negative `count`, the behavior changes and the command is allowed to return the same element multiple times. In this case, the number of returned elements is the absolute value of the specified `count`.

The optional `WITHSCORES` modifier changes the reply so it includes the respective scores of the randomly selected elements from the sorted set.

## Return Values

- [Bulk string reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#bulk-strings): when called without the `count` argument,
  returns the random member or `nil` if `key` does not exist.
- [Array reply](https://redis.io/docs/latest/develop/reference/protocol-spec/#arrays): when called with the `count` argument,
  returns the random members, or an empty array if `key` does not exist.
  If the `WITHSCORES` modifier is used, the reply is a list of members and their scores from the sorted set.

## Code Examples

```shell
dragonfly$> ZADD numbers 1 one 2 two 3 three 4 four
(integer) 4

# Returns a single random member.
dragonfly$> ZRANDMEMBER numbers
1) "one"

# Return multiple random members.
dragonfly$> ZRANDMEMBER numbers 2
1) "two"
2) "three"

# Return multiple random members (allowed to return the same element multiple times).
dragonfly$> ZRANDMEMBER numbers -3
1) "three"
2) "three"
3) "four"

# Return multiple random members with scores.
dragonfly$> ZRANDMEMBER numbers 3 WITHSCORES
1) "two"
2) "2"
3) "three"
4) "3"
5) "four"
6) "4"

# Return nil or an empry array on non-existent keys.
dragonfly$> ZRANDMEMBER non-existent
(nil)

dragonfly$> ZRANDMEMBER non-existent 10
(empty array)

dragonfly$> ZRANDMEMBER non-existent 10 WITHSCORES
(empty array)
```
