---
description:  Learn how to use Redis ZREVRANK to determine the index of a member in a sorted set, with scores ordered from high to low.
---

import PageTitle from '@site/src/components/PageTitle';

# ZREVRANK

<PageTitle title="Redis ZREVRANK Command (Documentation) | Dragonfly" />

## Syntax

    ZREVRANK key member

**Time complexity:** O(log(N))

**ACL categories:** @read, @sortedset, @fast

Returns the rank of `member` in the sorted set stored at `key`, with the scores
ordered from high to low.
The rank (or index) is 0-based, which means that the member with the highest
score has rank `0`.

The optional `WITHSCORE` argument supplements the command's reply with the score of the element returned.

Use `ZRANK` to get the rank of an element with the scores ordered from low to
high.

## Return

* If `member` exists in the sorted set [Integer reply](https://redis.io/docs/reference/protocol-spec/#integers): the rank of `member`.
* If `member` does not exist in the sorted set or `key` does not exist [Bulk string reply](https://redis.io/docs/reference/protocol-spec/#bulk-strings): `nil`.

## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZREVRANK myzset "one"
(integer) 2
dragonfly> ZREVRANK myzset "four"
(nil)
```
