---
description: Determine the index of a member in a sorted set
---

# ZRANK

## Syntax

    ZRANK key member

**Time complexity:** O(log(N))

**ACL categories:** @read, @sortedset, @fast

Returns the rank of `member` in the sorted set stored at `key`, with the scores
ordered from low to high.
The rank (or index) is 0-based, which means that the member with the lowest
score has rank `0`.

The optional `WITHSCORE` argument supplements the command's reply with the score of the element returned.

Use `ZREVRANK` to get the rank of an element with the scores ordered from high
to low.

## Return

* If `member` exists in the sorted set [Integer reply](https://redis.io/docs/reference/protocol-spec#resp-integers): the rank of `member`.
* If `member` does not exist in the sorted set or `key` does not exist [Bulk string reply](https://redis.io/docs/reference/protocol-spec#resp-bulk-strings): `nil`.
  
## Examples

```shell
dragonfly> ZADD myzset 1 "one"
(integer) 1
dragonfly> ZADD myzset 2 "two"
(integer) 1
dragonfly> ZADD myzset 3 "three"
(integer) 1
dragonfly> ZRANK myzset "three"
(integer) 2
dragonfly> ZRANK myzset "four"
(nil)
```
